def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a model'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		dest='model',
		required=True,
		help='ID of model to inspect'
	)

async def main(args):
	return await args.client.get(args.model)
