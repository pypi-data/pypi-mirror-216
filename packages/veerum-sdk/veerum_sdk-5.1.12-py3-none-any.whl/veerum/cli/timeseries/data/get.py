def add_arguments(subparser):
	parser = subparser.add_parser(
		'get',
		description='Get the data associated with a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to get data for'
	)

async def main(args):
	return await args.client.get_data(args.timeseries)
