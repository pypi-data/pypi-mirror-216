def add_arguments(subparser):
	parser = subparser.add_parser(
		'join',
		description='Add a user to an workscope'
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
		'-w',
		'--workscope',
		dest='workscope',
		required=True,
		help='ID of workscope to join'
	)

async def main(args):
	return await args.client.join_workscope(
		args.user,
		args.workscope
	)
