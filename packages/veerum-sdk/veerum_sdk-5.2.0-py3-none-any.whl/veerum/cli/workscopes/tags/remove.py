def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Remove a tag from a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='Work scope to remove the tag from'
	)
	parser.add_argument(
		'-t',
		'--tag',
		required=True,
		help='The tag to remove from the workscope'
	)

async def main(args):
	return await args.client.remove_tag(args.workscope, args.tag)
