def add_arguments(subparser):
	parser = subparser.add_parser(
		'add',
		description='Add a feature to a workscope'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='Workscope to add the feature to'
	)
	parser.add_argument(
		'-f',
		'--feature',
		required=True,
		choices=['viewer', 'progress'],
		help='The feature to add to the workscope'
	)

async def main(args):
	return await args.client.add_feature(args.workscope, args.feature)
