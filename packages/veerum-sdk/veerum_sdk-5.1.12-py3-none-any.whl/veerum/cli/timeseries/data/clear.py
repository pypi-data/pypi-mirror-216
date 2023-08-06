def add_arguments(subparser):
	parser = subparser.add_parser(
		'clear',
		description='Remove all the data associated with a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to get data for'
	)

async def main(args):
	return await args.client.clear_data(args.timeseries)
