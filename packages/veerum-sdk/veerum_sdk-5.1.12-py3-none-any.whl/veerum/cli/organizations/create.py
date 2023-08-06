def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a new organization'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-n',
		'--name',
		required=True,
		help=''
	)
	parser.add_argument(
		'-s',
		'--slug',
		required=True,
		help=''
	)
	parser.add_argument(
		'--99',
		dest='ninenine',
		default=False,
		action='store_true',
		help=''
	)
	parser.add_argument(
		'-l',
		'--nonUseLockPeriodDays',
		default=None,
		help='A period of inactivity in days when the user account should be locked'
	)
	parser.add_argument(
		'-e',
		'--pwdExpiresInDays',
		default=None,
		help='Amount of the days that a user password should expire'
	)
	parser.add_argument(
		'-a',
		'--maxLockoutAttempts',
		default=None,
		help='Total amount attempts of incorrect password input before the user will be locked out on some period'
	)
	parser.add_argument(
		'-ti',
		'--timeOfInactivityInSecs',
		default=None,
		help='Amount of seconds before logging of the app automatically'
	)
	parser.add_argument(
		'-acid',
		'--auth0ConnId',
		default=None,
		help='Auth0 connection ID required for SSO'
	)
	parser.add_argument(
		'-clientid',
		'--auth0ClientId',
		default=None,
		help='Auth client ID required for SSO'
	)
	parser.add_argument(
		'-rlu',
		'--rateLimitUsers',
		default=None,
		help='To change the number of available API requests to list users per organization'
	)
	parser.add_argument(
		'-rla',
		'--rateLimitAnnotations',
		default=None,
		help='To change the number of available API requests to list annotations per organization'
	)
	parser.add_argument(
		'-rlf',
		'--rateLimitFiles',
		default=None,
		help='To change the number of available API requests to list files per organization'
	)
	parser.add_argument(
		'-rlm',
		'--rateLimitModels',
		default=None,
		help='To change the number of available API requests to list models per organization'
	)
	parser.add_argument(
		'-rlw',
		'--rateLimitWorkscopes',
		default=None,
		help='To change the number of available API requests to list workscopes per organization'
	)

async def main(args):
	# TODO: {KL} sanitize the slug
	return await args.client.create(
		name=args.name,
		slug=args.slug,
		ninenine=args.ninenine,
		nonUseLockPeriodDays=args.nonUseLockPeriodDays,
		pwdExpiresInDays=args.pwdExpiresInDays,
		maxLockoutAttempts=args.maxLockoutAttempts,
		timeOfInactivityInSecs=args.timeOfInactivityInSecs,
		auth0ConnId=args.auth0ConnId,
		auth0ClientId=args.auth0ClientId,
		rateLimitUsers=args.rateLimitUsers,
		rateLimitAnnotations=args.rateLimitAnnotations,
		rateLimitFiles=args.rateLimitFiles,
		rateLimitModels=args.rateLimitModels,
		rateLimitWorkscopes=args.rateLimitWorkscopes
	)
