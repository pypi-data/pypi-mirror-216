def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for integrations'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		required=True,
		help='List integration used by an organization'
	)

async def main(args):
	return await args.client.get_integrations(args.organization)
