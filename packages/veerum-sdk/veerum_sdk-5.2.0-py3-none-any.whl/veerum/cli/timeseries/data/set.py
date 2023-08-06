def add_arguments(subparser):
	parser = subparser.add_parser(
		'set',
		description='Set the data points associate with a timeseries'
	)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to get data for'
	)
