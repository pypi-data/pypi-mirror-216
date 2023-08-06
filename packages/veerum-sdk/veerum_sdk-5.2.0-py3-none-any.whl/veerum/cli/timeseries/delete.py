def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to delete'
	)

async def main(args):
	return await args.client.delete(args.timeseries)
