def add_arguments(subparser):
	parser = subparser.add_parser(
		'clear',
		description='Remove all keys from a model\'s metadata'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		required=True,
		help='Model to remove keys from'
	)


async def main(args):
	return await args.client.clear_keys(args.model)
