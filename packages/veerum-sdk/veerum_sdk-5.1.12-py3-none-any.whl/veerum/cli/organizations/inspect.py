def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect an organization'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-o',
		'--organization',
		dest='organization',
		required=True,
		help='ID of organization to inspect'
	)

async def main(args):
	return await args.client.get(args.organization)
