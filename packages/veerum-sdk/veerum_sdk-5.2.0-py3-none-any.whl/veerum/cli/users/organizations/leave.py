def add_arguments(subparser):
	parser = subparser.add_parser(
		'leave',
		description='Remove a user from an organization'
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
		help='ID of organization to leave'
	)

async def main(args):
	return await args.client.leave_organization(
		args.user,
		args.organization
	)
