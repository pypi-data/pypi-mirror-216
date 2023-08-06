def add_arguments(subparser):
	parser = subparser.add_parser(
		'leave',
		description='Remove a user from an workscope'
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
		help='ID of workscope to leave'
	)

async def main(args):
	return await args.client.leave_workscope(
		args.user,
		args.workscope
	)
