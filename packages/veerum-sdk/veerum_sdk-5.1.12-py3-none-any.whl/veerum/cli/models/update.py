from datetime import datetime


def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Modify a model'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		dest='model',
		required=True,
		help='ID of model to modify'
	)
	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='ID of the workscope this model should be attached to'
	)
	parser.add_argument(
		'-d',
		'--date',
		default=None,
		type=datetime.fromisoformat,
		help='Date the data for the model was acquired (ISO8601 format)'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Name of the model'
	)
	parser.add_argument(
		'--description',
		default=None,
		help='Description of the model'
	)
	parser.add_argument(
		'--type',
		choices=['actual', 'design', 'computed'],
		default=None,
		help='The type of the model'
	)
	parser.add_argument(
		'--category',
		default=None,
		help='The category of the model'
	)
	parser.add_argument(
		'--auto2d',
		default=None,
		help="True to enable auto2D for this model, False to disable. By default it is left without changes"
	)

async def main(args):
	return await args.client.update(
		args.model,
		workscope=args.workscope,
		date=args.date,
		name=args.name,
		description=args.description,
		type=args.type,
		category=args.category,
		auto2d=args.auto2d
	)
