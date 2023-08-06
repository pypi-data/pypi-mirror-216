def add_arguments(subparser):
	parser = subparser.add_parser(
		'add',
		description='Add a key to a model\'s metadata'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		required=True,
		help='Model with metadata to add the key to'
	)
	parser.add_argument(
		'-k',
		'--key',
		required=True,
		help='The key to add to the metadata'
	)


async def main(args):
	return await args.client.add_key(args.model, args.key)
