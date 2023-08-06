def add_arguments(subparser):
	parser = subparser.add_parser(
		'inspect',
		description='Inspect a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		dest='timeseries',
		required=True,
		help='ID of timeseries to inspect'
	)

async def main(args):
	return await args.client.get(args.timeseries)
