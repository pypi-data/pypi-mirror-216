import os
import pathlib
import csv
import json

from tqdm import tqdm
from . import fileparser


def add_arguments(subparser):
		parser = subparser.add_parser(
				'ingest',
				description='Ingest one or many csv files representing Objects. Must ref model OR workscope (not BOTH or NEITHER)',
		)
		parser.set_defaults(command=main)

		parser.add_argument(
				'-o',
				'--organization',
				required=True,
				help='ID of the Organization this paper object should be attached to (Required)'
		)

		parser.add_argument(
				'-w',
				'--workscope',
				required=True,
				help='ID of the Workscope this paper object should be attached to (Required)'
		)
		
		parser.add_argument(
				'-fi',
				'--file',
				required=True,
				help='ID of the file this paper object should be attached to (Required)'
		)
		
		parser.add_argument(
				'-f',
				'--format',
				required=True,
				choices=['json', 'csv'],
				help='Desirable format of files to import.'
		)

		parser.add_argument('path', help='Path to csv files for upload')

# throttles payload to API based on max # of metadata in objects 
def throttle_bunchsize(max_metadata_count):
		bunch_size_min = 1          # min number of objects per request
		bunch_size_max = 100         # max number of objects per request
		bunch_size_adjusted = round(bunch_size_max / (max_metadata_count / 10))
		if (bunch_size_adjusted < bunch_size_min):
				bunch_size_adjusted = bunch_size_min
		elif (bunch_size_adjusted > bunch_size_max):
				bunch_size_adjusted = bunch_size_max

		return bunch_size_adjusted

def count_max(metadata):
		return len(metadata)
		
async def main(args):
		args.path = os.path.normpath(args.path)
		organization = args.organization,
		workscope = args.workscope,
		file = args.file,
		
		max_count = 1 # updated later in the code with the max # of metadata / object
		max_text_length = 50 # Split text into a 20 char text

		job_log = tqdm(total=0, bar_format='{desc}')
		
		# validate files
		job_log.set_description_str('Validating')
		selected = list(validate_files(fileparser.select_files(args.path, args.format)))
		#  check amount of files
		if len(selected) == 0:
				error = f'Error: there are no {args.format} files under the path'
				job_log.set_description_str(error)
				job_log.close()
				return False

		selected.sort()

		# parse csv or json files for uploading
		job_log.set_description_str('Parsing')
		objects_to_upload = []

		if args.format == 'csv':
				for obj in selected:
						with open(obj.path, encoding="utf-8-sig") as csv_file:
								csv_reader = csv.reader(csv_file, delimiter=',')
								paperObjects = []
								for row in csv_reader:
										paperObjects.append({
												'text': row[0],
												'bbox': row[1],
												'page': row[2],
												'object_id': row[3],
												'file_id': file,
												'organizationId': organization,
												'workscopeId': workscope,
												
										})
								paperObjects_json = json.dumps(paperObjects)
								count = count_max(paperObjects_json)
								if count > max_count:
										max_count = count

								objects_to_upload = paperObjects_json
		else:
				for obj in selected:
						with open(obj.path, encoding="utf-8-sig") as json_file:
								json_reader = json.load(json_file)
								#  check if file is for a single object or for multiple
								paper = []
								for objects in (json_reader if isinstance(json_reader[0], list) else [json_reader]):
										modifiedPaper = {}
										bbox = [0, 0, 0, 0]
										for object in objects:
											if object['key'] == 'x':
												bbox[0] = object['value']
											if object['key'] == 'y':
												bbox[1] = object['value']
											if object['key'] == 'width':
												bbox[2] = object['value']
											if object['key'] == 'height':
												bbox[3] = object['value']
											if object['key'] == 'name':
												modifiedPaper['text'] = object['value'][:max_text_length]

											if object['key'] == 'page':
												modifiedPaper['page'] = object['value']

											if object['key'] == 'object':
												modifiedPaper['object_id'] = object['value']

											if all(x > 0 for x in bbox):
												modifiedPaper['bbox'] = bbox
										
										if 'paper' not in modifiedPaper:
											modifiedPaper['page'] = 1

										if 'bbox' and 'text' and 'page' in modifiedPaper:
											modifiedPaper['file_id'] = file[0]
											modifiedPaper['organizationId'] = organization[0]
											modifiedPaper['workscopeId'] = workscope[0]
											paper.append(modifiedPaper)
										
								paperObjects_json = paper
								count = count_max(paperObjects_json)
								if count > max_count:
										max_count = count
										
								objects_to_upload = paperObjects_json

		# throttle upload payload based on max # of metadata per Object found
		bunch_size_adjusted = throttle_bunchsize(max_count)

		# upload files
		n = 0
		bunch = []
		job_log.set_description_str('Ingesting')
		progress = tqdm(total=len(objects_to_upload), unit=' Paper Objects Ingested', position=0, leave=True)

		# shared function to import objects
		async def bulk_create(objects):
				veerum_object = await args.client.bulk_create(objects)

				try:
						# handling expected errors
						if ('data' not in veerum_object):
								job_log.set_description_str("Error: Bulk upload error. Details: {0}".format(veerum_object))
								job_log.close()
								progress.close()
								return 'failed'
				except:
						# handling unexpected errors
						job_log.set_description_str("Error: {0}".format(veerum_object))
						job_log.close()
						progress.close()
						return 'unknown error'

				return 'success'
		
		for obj in objects_to_upload:
				n += 1
				bunch.append(obj)
				if n % bunch_size_adjusted == 0:
						import_result = await bulk_create(bunch)  # importing process
						if import_result != 'success':
								return import_result
						progress.update(bunch_size_adjusted)  # update progress bar
						progress.set_description('')
						bunch = []  # reinitialize array
						# time.sleep(1.5) # timeout to reduce load to API

		if len(bunch) != 0:
				# upload the rest objects
				import_result = await bulk_create(bunch)  # importing process
				if import_result != 'success':
						return import_result
				progress.update(len(bunch))  # update progress bar

		job_log.set_description_str('Ingestion Results:')
		job_log.close()
		progress.close()
		return 'success'


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