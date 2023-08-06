import os
import signal
import asyncio
import logging
import pathlib
import csv
import json
import time

from datetime import datetime

from tornado import gen, ioloop, locks, queues
from tqdm import tqdm

from . import csvparser

from ... import retcode

def add_arguments(subparser):
	parser = subparser.add_parser(
		'upload',
		description='Upload metadata to a model',
	)
	parser.set_defaults(command=main)

	parser = subparser.add_parser(
		'upload_test',
		description='Upload metadata to a model',
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		help='Model the metadata should be associated with'
	)
	# parser.add_argument(
	# 	'-d',
	# 	'--date',
	# 	required=True,
	# 	type=datetime.fromisoformat,
	# 	help='Date the data for the metadata was acquired (ISO8601 format)'
	# )
	# parser.add_argument(
	# 	'--description',
	# 	default=None,
	# 	help='Description (Optional)'
	# )
	parser.add_argument(
		'--dryrun',
		default=False,
		action='store_true',
		help='Just print the files that would be uploaded and exit'
	)

	parser.add_argument('metadata', help='Path to the metadata for upload')

async def main(args):
	args.metadata = os.path.normpath(args.metadata)

	job_log = tqdm(total=0, bar_format='{desc}')

	selected = list(validate_files(csvparser.select_files(args.metadata)))
	num_objects = len(selected)
	
	if args.dryrun:
		for obj in selected:
			print('{key:s} > update'.format(key=obj.key))
		return

	# validate files
	job_log.set_description_str(f'Validating')

	# parse csv files for upload
	job_log.set_description_str(f'Parsing')
	objects_to_upload = []
	for obj in selected:
		with open(obj.path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			metadata = []
			for row in csv_reader:
				metadata.append({
					'category': row[0],
					'key': row[1],
					'value': row[2]
				})
				# print(f'{", ".join(row)}')
			metadata_json = json.dumps(metadata)
			objects_to_upload.append({
				'file': obj.key,
				'metadata': metadata_json,
			})

	# upload files
	progress = tqdm(total=num_objects, unit='Object')

	for obj in objects_to_upload:

		filename = obj['file']
		job_log.set_description_str(f'Uploading: {filename}')

		veerum_object = await args.client.create_object(
			model=args.model,
			metadata=obj['metadata']
		)

		if not '_id' in veerum_object:
			job_log.set_description_str(f'Error: {filename}')
			job_log.close()
			progress.close()
			print(veerum_object['message'])
			return('failed')

		progress.update(1)

		# TODO: remove time.sleep once API is integrated
		# time.sleep(0.5)

	job_log.set_description_str(f'Upload Complete')
	job_log.close()
	progress.close()
	return('success')

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
