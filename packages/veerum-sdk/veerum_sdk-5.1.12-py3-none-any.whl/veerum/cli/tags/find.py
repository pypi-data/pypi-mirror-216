def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for tags'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find tags attached to a workscope'
	)


async def main(args):
	return await args.client.find(
		workscope=args.workscope,
	)
