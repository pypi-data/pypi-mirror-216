def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete a milestone'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--milestone',
		required=True,
		help='ID of milestone to delete'
	)

async def main(args):
	return await args.client.delete(args.milestone)
