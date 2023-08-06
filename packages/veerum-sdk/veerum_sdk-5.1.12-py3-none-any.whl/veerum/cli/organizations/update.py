def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Modify an organization'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-o',
		'--organization',
		required=True,
		help='ID of organization to modify'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Name of the organization'
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
		help='Total attempts amount of incorrect password input before the user will be locked out on some period'
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
		'-dws',
		'--defaultOrgWs',
		help='Comma separated default workscope IDs. List of ws user has access to depending on his default ws rights',
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
	return await args.client.update(
		args.organization,
		name=args.name,
		nonUseLockPeriodDays=args.nonUseLockPeriodDays,
		pwdExpiresInDays=args.pwdExpiresInDays,
		maxLockoutAttempts=args.maxLockoutAttempts,
		timeOfInactivityInSecs=args.timeOfInactivityInSecs,
		auth0ConnId=args.auth0ConnId,
		auth0ClientId=args.auth0ClientId,
		defaultOrgWs=args.defaultOrgWs,
		rateLimitUsers=args.rateLimitUsers,
		rateLimitAnnotations=args.rateLimitAnnotations,
		rateLimitFiles=args.rateLimitFiles,
		rateLimitModels=args.rateLimitModels,
		rateLimitWorkscopes=args.rateLimitWorkscopes
	)
