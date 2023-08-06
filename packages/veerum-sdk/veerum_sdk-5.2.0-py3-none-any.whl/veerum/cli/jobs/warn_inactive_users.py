def add_arguments(subparser):
	parser = subparser.add_parser(
		'warn_inactive_users',
		description='Warn all inactive users that their account will be locked out'
	)
	parser.set_defaults(command=main)

async def main(args):
	return await args.client.warn_inactive_users()
