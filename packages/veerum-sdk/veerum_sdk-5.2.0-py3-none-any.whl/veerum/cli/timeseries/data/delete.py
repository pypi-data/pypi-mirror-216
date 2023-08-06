def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Remove a single data point from a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to remove data from'
	)

	parser.add_argument(
		'-d',
		'--data',
		required=True,
		help='ID of data point to remove'
	)

async def main(args):
	return await args.client.remove_data(args.timeseries, args.data)
