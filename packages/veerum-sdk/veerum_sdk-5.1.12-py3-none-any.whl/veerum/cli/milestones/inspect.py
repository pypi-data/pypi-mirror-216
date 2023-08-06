def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a milestone'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--milestone',
		dest='milestone',
		required=True,
		help='ID of milestone to inspect'
	)

async def main(args):
	return await args.client.get(args.milestone)
