def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete tags from a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='ID of workscope to delete'
	)

async def main(args):
	return await args.client.delete(args.workscope)
