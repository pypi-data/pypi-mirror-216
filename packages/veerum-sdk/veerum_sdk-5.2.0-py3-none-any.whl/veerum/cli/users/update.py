def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Modify a user'
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
		'-e',
		'--email',
		dest='user_email',
		default=None,
		help='Updated email address for the user'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='New name of the user'
	)
	parser.add_argument(
		'-p',
		'--phone',
		default=None,
		help='New phone number for the user'
	)
	parser.add_argument(
		'-d',
		'--disabled',
		default=None,
		help='Enable / disable the user'
	)
	parser.add_argument(
		'-sso',
		'--sso',
		default=None,
		help='Enable / disable SSO login workflow'
	)
	parser.add_argument(
		'-vr',
		'--wsViewRights',
		choices=['none', 'default', 'all'],
		help='Workscope access rights',
	)

async def main(args):
	return await args.client.update(
		args.user,
		email=args.user_email,
		name=args.name,
		phone=args.phone,
		disabled=args.disabled,
		sso=args.sso,
		wsViewRights=args.wsViewRights,
	)
