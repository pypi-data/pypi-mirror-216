def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		dest='workscope',
		required=True,
		help='ID of workscope to inspect'
	)

async def main(args):
	return await args.client.get(args.workscope)
