def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect an annotation'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-a',
		'--annotation',
		required=True,
		help='ID of annotation to inspect'
	)

async def main(args):
	return await args.client.get(args.annotation)
