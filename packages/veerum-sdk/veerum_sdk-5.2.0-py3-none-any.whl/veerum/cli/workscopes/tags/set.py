def add_arguments(subparser):
	parser = subparser.add_parser(
		'set',
		description='Replace the tags on a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='Work scope to add the tag to'
	)
	parser.add_argument(
		'-t',
		'--tag',
		default=[],
		nargs='+',
		help='The tags to set on the workscope'
	)

async def main(args):
	return await args.client.set_tags(args.workscope, *args.tag)
