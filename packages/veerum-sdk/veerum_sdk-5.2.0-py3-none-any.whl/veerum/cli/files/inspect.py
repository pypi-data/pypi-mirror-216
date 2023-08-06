def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-f',
		'--file',
		dest='file',
		required=True,
		help='ID of file to inspect'
	)

async def main(args):
	return await args.client.get(args.file)
