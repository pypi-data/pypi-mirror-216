def add_arguments(subparser):
	parser = subparser.add_parser(
		'join',
		description='Add a user to an organization'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-u',
		'--user',
		dest='user',
		required=True,
		help='ID of user to modify'
	)
	parser.add_argument(
		'-o',
		'--organization',
		dest='organization',
		required=True,
		help='ID of organization to join'
	)

async def main(args):
	return await args.client.join_organization(
		args.user,
		args.organization
	)
