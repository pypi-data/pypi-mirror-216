import os
import signal
import asyncio
import gzip
import logging
import pathlib

from datetime import datetime

from tornado import gen, ioloop, locks, queues
from tqdm import tqdm
from tusclient import client as tus

from . import potree
from . import potree2
from . import unity
from . import tiles

from ... import retcode

def add_arguments(subparser):
	parser = subparser.add_parser(
		'upload',
		description='Upload model(s)',
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		help='ID of the workscope this model should be attached to.'
	)
	parser.add_argument(
		'-m',
		'--model',
		help='ID of the parent model these models should be related to.'
	)
	parser.add_argument(
		'-d',
		'--date',
		required=True,
		type=datetime.fromisoformat,
		help='Date the data for the model was acquired (ISO8601 format)'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='''
			Name of the model. If not present defaults to the last
			part of the path in the model argument.
		'''
	)
	parser.add_argument(
		'--format',
		choices=['potree', 'potree2', 'unity', 'draco', '3d-tiles'],
		required=True,
		help='Format of the model'
	)
	parser.add_argument(
		'--type',
		choices=['actual', 'design', 'computed'],
		required=True,
		help='Find models by type'
	)
	parser.add_argument(
		'--category',
		default=None,
		help='Model category (Optional)'
	)
	parser.add_argument(
		'--description',
		default=None,
		help='Description of the file (Optional)'
	)

	parser.add_argument(
		'--dryrun',
		default=False,
		action='store_true',
		help='Just print the files that would be uploaded and exit'
	)

	parser.add_argument(
		'--workers',
		default=1,
		type=int,
		help='The number of concurrent uploads to use'
	)

	parser.add_argument(
		'--auto2d',
		default=False,
		help="True to enable auto2D for this model, False to disable"
	)

	parser.add_argument(
		'--gzip',
		default=False,
		help="True if all upload files are compressed with gzip, false if uncompressed, only available for 3d-tiles format"
	)

	parser.add_argument('model', help='Path to a model to upload')

SELECTORS = {
	'potree': potree.select_files,
	'potree2': potree2.select_files,
	'unity': unity.select_files,
	'3d-tiles': tiles.select_files,
}

def shutdown_wrapper(event):
	def shutdown_handler(signum, frame):
		logging.info('Shutdown signal recieved')
		logging.info('!...Please wait while CLI cleans up...!')
		event.set()
		

	return shutdown_handler

async def main(args):
	if not args.format in SELECTORS:
		logging.error('The model format %s is not currently supported', args.format)
		return retcode.NOT_IMPLEMENTED
	
	if args.gzip and args.format != '3d-tiles':
		logging.error('The model format %s does not support gzip', args.format)
		return retcode.NOT_IMPLEMENTED

	args.model = os.path.normpath(args.model)
	if args.name is None:
		args.name = os.path.basename(args.model).strip()
		if not args.name:
			args.name = 'Untitled'

	args.workers = max(1, args.workers)

	selected = list(validate_files(SELECTORS[args.format](args.model)))

	if args.gzip and len(selected) > 0:
		for file in selected:
			with gzip.open(file.path, 'rb') as f:
				try:
					f.read(1)
				except OSError as e:
					logging.error('The model file: %s is not compressed with gzip', file.path)
					return retcode.GENERAL_ERROR

	if args.dryrun:
		for obj in selected:
			print('{path:s} > {key:s}'.format(path=obj.path, key=obj.key))
		return

	sizes = {obj.key:os.path.getsize(obj.path) for obj in selected}
	progress = tqdm(total=sum(sizes.values()), unit='B', unit_scale=True, unit_divisor=1024)

	# TODO: {KL} If any of this fails rollback the upload

	model = await args.client.create(
		workscope=args.workscope,
		date=args.date,
		format=args.format,
		type=args.type,
		name=args.name,
		description=args.description,
		category=args.category,
	)
	if not '_id' in model:
		return model

	if args.format == '3d-tiles' and len(selected) > 0:
		rootTileJsonMetadata = [{
			'category': 'vrm:internal',
			'key': 'vrm:root-tile-json',
			'value': os.path.basename(selected[0].path)
		}]
		model['metadata'] = await args.client.set_metadata(model['_id'], rootTileJsonMetadata)

	q = queues.Queue()
	shutdown = locks.Event()
	workers = gen.multi([worker(q, args.client, shutdown, sizes, progress) for _ in range(args.workers)])

	# Attach an interrupt handler for clean shutdown
	signal.signal(signal.SIGINT, shutdown_wrapper(shutdown))

	for source in selected:
		upload = {
			'model': model['_id'],
			'key': source.key,
			'filename': source.path,
			'mimetype': source.mimetype,
			'encoding': 'gzip' if args.gzip else 'identity'
		}
		await q.put(upload)

	await asyncio.wait([q.join(), shutdown.wait()], return_when=asyncio.FIRST_COMPLETED)

	# Signal all workers to exit
	for _ in range(args.workers):
		await q.put(None)

	await workers

	for result in workers.result():
		if result is not None and result != 0:
			return result
	
	return model

async def worker(queue, client, shutdown, sizes, progress=None):
	async for upload in queue:
		if upload is None:
			return
		if shutdown.is_set():
			return retcode.GENERAL_ERROR

		if(upload['key'] == 'octree.bin'):
			model_id = upload['model']
			tus_url = f'{client.endpoint}/models/{model_id}/tus'
			auth_string = f'Bearer {client.get_token()}'

			# This chunk_size must match the partSize in the node tus server S3Store
			chunk_size = 32 * 1024 * 1024
			if sizes[upload['key']] / chunk_size >= 10000:
				chunk_size *= 2
			tus_client = tus.TusClient(tus_url, headers={'Authorization': auth_string, 'part-size': str(chunk_size)})

			abort_upload = False

			try:
				uploader = tus_client.uploader(
					upload['filename'],
					chunk_size=chunk_size,
					# Only needed to stop server complaining about no metadata
					metadata={'modelId': model_id},
					retries=3,
					retry_delay=10
				)

				while uploader.offset < uploader.file_size:
					uploader.upload_chunk()
					progress.update(chunk_size)
					if shutdown.is_set():
						abort_upload = True

			except Exception as ex:
				abort_upload = True
				logging.info('Error with S3 multipart upload...')
				logging.exception(ex)
			finally:
				queue.task_done()
				if abort_upload:
					logging.info('Aborting S3 multipart upload...')
					await client.abort_multipart(model_id)
					return retcode.GENERAL_ERROR
				else:
					logging.info('Done!')
		else:
			try:
				logging.debug(upload)
				await client.upload_file(**upload)
				progress.update(sizes[upload['key']])
			except FileNotFoundError:
				logging.error('FileNotFoundError: %s', upload['filename'])
			except Exception as ex:
				logging.exception(ex)
				# Retry the upload later
				await queue.put(upload)
			finally:
				queue.task_done()

def validate_files(files):
	for file in files:
		if not os.path.exists(file.path):
			raise Exception()
		if not os.path.isfile(file.path):
			raise Exception()

		syspath = pathlib.Path(file.key)
		nixpath = pathlib.PurePosixPath(syspath)

		# This is here to fix a windows to unix path conversion issue
		file = file._replace(key=str(nixpath))

		yield file
