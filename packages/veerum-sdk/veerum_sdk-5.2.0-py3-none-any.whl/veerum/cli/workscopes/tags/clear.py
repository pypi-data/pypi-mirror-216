def add_arguments(subparser):
	parser = subparser.add_parser(
		'clear',
		description='Remove all tags from a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='Work scope to remove tags from'
	)

async def main(args):
	return await args.client.clear_tags(args.workscope)
