def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete a model'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		required=True,
		help='ID of model to delete'
	)

async def main(args):
	return await args.client.delete(args.model)
