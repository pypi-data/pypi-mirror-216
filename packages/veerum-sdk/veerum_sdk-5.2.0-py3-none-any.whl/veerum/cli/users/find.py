from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for users'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-e',
		'--email',
		dest='username',
		default=None,
		help='Find users by email address'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Find users by name'
	)
	parser.add_argument(
		'-p',
		'--phone',
		default=None,
		help='Find users by phone number'
	)

	parser.add_argument(
		'-P',
		'--pwned',
		default=None,
		help='Find all users with passwords that have been pwned'
	)

	supports_sorting(parser, 'email', 'name', 'pwned')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		email=args.username,
		name=args.name,
		phone=args.phone,
		pwned=args.pwned,
		sort=args.sort,
		order=args.order,
		offset=args.skip,
		limit=args.limit
	)
