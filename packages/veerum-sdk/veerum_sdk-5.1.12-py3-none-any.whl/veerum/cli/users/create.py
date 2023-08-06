def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a new user'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-e',
		'--email',
		dest='username',
		required=True,
		help=''
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help=''
	)
	parser.add_argument(
		'-p',
		'--phone',
		default=None,
		help=''
	)
	parser.add_argument(
		'-w',
		'--workscopes',
		help='Comma separated workscope IDs',
	)
	parser.add_argument(
		'-o',
		'--organizations',
		help='Comma separated organization IDs',
	)
	parser.add_argument(
		'-vr',
		'--wsViewRights',
		choices=['none', 'default', 'all'],
		help='Workscope access rights',
	)

async def main(args):
	return await args.client.create(
		email=args.username,
		name=args.name,
		phone=args.phone,
		workscopes=args.workscopes,
		organizations=args.organizations,
		wsViewRights=args.wsViewRights,
	)
