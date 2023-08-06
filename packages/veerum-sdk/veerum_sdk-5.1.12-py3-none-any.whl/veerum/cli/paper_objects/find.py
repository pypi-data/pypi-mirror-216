from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for objects'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-f',
		'--file',
		default=None,
		required=True,
		help='Find paper objects attached to a file ID'
	)

	parser.add_argument(
		'-o',
		'--object',
		default=None,
		help='Find paper objects attached to a file ID'
	)
	supports_sorting(parser, 'text', 'page', 'createdAt', 'createdat', 'model', 'workscope', 'file', 'object')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		file=args.file,
		object=args.object if args.object else None,
		sort=args.sort,
		order=args.order,
		skip=args.skip,
		limit=args.limit
	)
