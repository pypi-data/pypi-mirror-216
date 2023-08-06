def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect metadata for a model'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		dest='model',
		required=True,
		help='Model\'s metadata to inspect'
	)


async def main(args):
	return await args.client.get(args.model)
