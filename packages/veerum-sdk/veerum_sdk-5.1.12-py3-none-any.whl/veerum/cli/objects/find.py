from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for objects'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find objects attached to a workscope'
	)

	parser.add_argument(
		'-m',
		'--model',
		default=None,
		help='Find objects attached to a model'
	)

	supports_sorting(parser, 'name', 'createdAt', 'createdat', 'model', 'workscope')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		model=args.model,
		sort=args.sort,
		order=args.order,
		skip=args.skip,
		limit=args.limit
	)
