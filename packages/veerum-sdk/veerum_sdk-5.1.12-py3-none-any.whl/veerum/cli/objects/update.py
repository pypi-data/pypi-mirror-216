import os
import csv
import json

from . import fileparser
def nullable_float(str):
	if str == "":
		return None
	else:
		return float(str)

def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Modify an object'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-oid',
		'--object',
		required=True,
		help='ID of object to update'
	)
	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'-m',
		'--model',
		default=None,
		help='ID of model to relate Object to'
	)
	group.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='ID of workscope to relate Object to'
	)
	parser.add_argument(
		'-p',
		'--position',
		type=nullable_float,
		nargs='*',
		help='Center object at [x=0,y=1,z=2]'
	)
	parser.add_argument(
		'-s',
		'--scale',
		type=nullable_float,
		nargs='*',
		help='Scale of object for each x,y,z axis'
	)
	parser.add_argument(
		'-o',
		'--orientation',
		type=nullable_float,
		nargs='*',
		help='Rotation object around each x,y,z axis'
	)

	parser.add_argument(
		'-f',
		'--format',
		choices=['json', 'csv'],
		help='Desirable format of the metadata file'
	)

	parser.add_argument(
		'--metadata',
		default=None,
		help='Path to JSON or CSV file containing new category, key, value for Object'
	)

async def main(args):
	metadata_json = []

	if args.metadata and args.format is None:
		raise Exception('--format argument is required while using --metadata')
	elif args.format and args.metadata is None:
		raise Exception('--metadata argument is required while using --format')
	elif args.format and args.metadata:
		args.metadata = os.path.normpath(args.metadata)
		selected = fileparser.validate_file(fileparser.select_file(args.metadata, args.format))

		if args.format == 'csv':
			with open(selected.path, encoding="utf-8-sig") as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				metadata_json = []
				for row in csv_reader:
					metadata_json.append({
						'category': row[0],
						'key': row[1],
						'value': row[2]
					})

		else:
			with open(selected.path, encoding="utf-8-sig") as json_file:
				json_reader = json.load(json_file)
				# if there is an array of arrays - use the first element otherwise use all objects in the array to do API request
				for object in (json_reader[0] if isinstance(json_reader[0], list) else json_reader):
					metadata_json.append(object)

	return await args.client.update(
		args.object,
		model=args.model,
		workscope=args.workscope,
		position=args.position,
		scale=args.scale,
		orientation=args.orientation,
		metadata=metadata_json if len(metadata_json) > 0 else None
	)
