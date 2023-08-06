from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for organizations'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Find organizations with a matching name'
	)

	supports_sorting(parser, 'name')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		name=args.name,
		sort=args.sort,
		order=args.order,
		offset=args.skip,
		limit=args.limit
	)
