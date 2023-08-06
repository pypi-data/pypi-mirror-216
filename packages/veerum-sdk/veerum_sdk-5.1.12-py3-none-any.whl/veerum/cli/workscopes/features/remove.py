def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Remove a feature from a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='Work scope to remove the feature from'
	)
	parser.add_argument(
		'-f',
		'--feature',
		required=True,
		help='The feature to remove from the workscope'
	)

async def main(args):
	return await args.client.remove_feature(args.workscope, args.feature)
