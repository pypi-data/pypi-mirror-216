def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a user'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-u',
		'--user',
		dest='user',
		required=True,
		help='ID of user to inspect'
	)

async def main(args):
	return await args.client.get(args.user)
