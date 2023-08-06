def add_arguments(subparser):
	parser = subparser.add_parser(
		'set',
		description='Replace the keys on a model\'s metadata'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		required=True,
		help='Model\'s metadata to add the key to'
	)
	parser.add_argument(
		'-k',
		'--key',
		default=[],
		nargs='+',
		help='The keys to set on the metadata'
	)


async def main(args):
	return await args.client.set_keys(args.model, *args.key)
