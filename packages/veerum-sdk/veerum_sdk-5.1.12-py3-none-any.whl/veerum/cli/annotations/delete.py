def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete an annotation'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-a',
		'--annotation',
		required=True,
		help='ID of annotation to delete'
	)

async def main(args):
	return await args.client.delete(args.annotation)
