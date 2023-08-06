import os
import signal
import asyncio
import logging
import json
from .. import fileparser
import sys

from tornado import gen, ioloop, locks, queues
from tqdm import tqdm

def add_arguments(subparser):
	parser = subparser.add_parser(
		'upload',
		description='Upload object pano(s)',
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'--workers',
		default=1,
		type=int,
		help='The number of concurrent uploads to use'
	)

	parser.add_argument(
		'-o',
		'--organization',
		help='ID of the parent organization these panos should be related to.',
		required=True
	)

	parser.add_argument(
		'-uuid',
		'--uuid',
		help='Unique ID generated randomly to accept different versions for the same directory',
		required=True
	)

	parser.add_argument('pano', help='Path to a pano to upload')

def shutdown_handler(event):
	def shutdown_callback():
		logging.info('Shutdown signal recieved')
		event.set()

	def wrapper(signum, frame):
		ioloop.IOLoop.current().add_callback_from_signal(shutdown_callback)

	return wrapper

async def main(args):
	args.workers = max(1, args.workers)

	args.pano = os.path.normpath(args.pano)
	selected = list(fileparser.validate_files(fileparser.select_pano_files(args.pano)))

	sizes = {obj.key:os.path.getsize(obj.path) for obj in selected}
	progress = tqdm(total=sum(sizes.values()), unit='B', unit_scale=True, unit_divisor=1024)

	q = queues.Queue()
	shutdown = locks.Event()
	workers = gen.multi([worker(q, args.client, shutdown, sizes, progress) for _ in range(args.workers)])

	# Attach an interrupt handler for clean shutdown
	signal.signal(signal.SIGINT, shutdown_handler(shutdown))

	for source in selected:
		# 33398dd1-f361-4ace-bfa4-5780134326e1 + def1111/222/abc33 + preview_111.jpg
		rel_path = os.path.join(args.uuid, os.path.relpath(source.path, args.pano)) # get relative path
		upload = {
			'organization': args.organization,
			'key': source.key,
			'filename': source.path,
			'rel_path': fileparser.as_posix_path(rel_path), # convert windows to unix path
			'mimetype': source.mimetype
		}
		await q.put(upload)

	await asyncio.wait([q.join(), shutdown.wait()], return_when=asyncio.FIRST_COMPLETED)

	# Signal all workers to exit
	for _ in range(args.workers):
		await q.put(None)

	await workers

	data = {}
	data['success'] = True
	data['s3Path'] = args.organization + '/' + args.uuid
	json_data = json.dumps(data)
	print(json_data)
	return

async def worker(queue, client, shutdown, sizes, progress=None):
	async for upload in queue:
		if upload is None or shutdown.is_set():
			return

		try:
			logging.debug(upload)
			result = await client.upload_file(**upload)

			if "statusCode" in result and result['statusCode'] == 404:
				# handling 404 errors
				logging.error('Organization not found or no access to it')
				sys.exit(1)

			progress.update(sizes[upload['key']])
		except FileNotFoundError:
			logging.error('FileNotFoundError: %s', upload['filename'])
		except Exception as ex:
			logging.exception(ex)
			# Retry the upload later
			await queue.put(upload)
		finally:
			queue.task_done()
