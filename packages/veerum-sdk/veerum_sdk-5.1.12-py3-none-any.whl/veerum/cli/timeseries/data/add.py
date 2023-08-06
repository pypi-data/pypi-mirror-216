from datetime import datetime

def add_arguments(subparser):
	parser = subparser.add_parser(
		'add',
		description='Add a new data point to a timeseries'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-t',
		'--timeseries',
		required=True,
		help='ID of timeseries to get data for'
	)

	parser.add_argument(
		'-x',
		required=True,
		type=datetime.fromisoformat,
		help='Date the data point was acquired (ISO8601 format)'
	)

	parser.add_argument(
		'-y',
		required=True,
		type=float,
		help='Value of the data point'
	)

async def main(args):
	return await args.client.add_data(args.timeseries, args.x, args.y)
