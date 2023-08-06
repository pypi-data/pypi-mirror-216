def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete a file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-f',
		'--file',
		required=True,
		help='ID of file to delete'
	)

async def main(args):
	return await args.client.delete(args.file)
