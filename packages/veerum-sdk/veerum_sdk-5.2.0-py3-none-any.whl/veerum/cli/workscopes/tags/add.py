def add_arguments(subparser):
	parser = subparser.add_parser(
		'add',
		description='Add a tag to a workscope'
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
		required=True,
		help='The tag to add to the workscope'
	)

async def main(args):
	return await args.client.add_tag(args.workscope, args.tag)
