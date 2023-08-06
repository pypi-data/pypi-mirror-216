from datetime import datetime

def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Modify a file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-f',
		'--file',
		dest='file',
		required=True,
		help='ID of file to modify'
	)
	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='ID of the workscope this file should be attached to'
	)
	parser.add_argument(
		'-d',
		'--date',
		type=datetime.fromisoformat,
		help='Date of the file (ISO8601 format)'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Name of the file'
	)
	parser.add_argument(
		'-D',
		'--description',
		default=None,
		help='Description of the file'
	)

async def main(args):
	return await args.client.update(
		args.file,
		workscope=args.workscope,
		date=args.date,
		name=args.name,
		description=args.description
	)
