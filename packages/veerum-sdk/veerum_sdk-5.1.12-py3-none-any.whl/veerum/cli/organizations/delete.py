def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete an organization'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-o',
		'--organization',
		required=True,
		help='ID of organization to modify'
	)

async def main(args):
	return await args.client.delete(
		args.organization
	)
