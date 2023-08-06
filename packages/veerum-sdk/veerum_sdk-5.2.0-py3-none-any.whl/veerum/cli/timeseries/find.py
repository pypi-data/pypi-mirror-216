from datetime import datetime

from ..common import supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for timeseries'
	)
	parser.set_defaults(command=main, current=None)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find timeseries attached to a workscope'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find timeseries attached to an organization'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Find timeseries with a matching name'
	)
	parser.add_argument(
		'--type',
		default=None,
		help='Find timeseries by type'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'--current',
		dest='current',
		action='store_true',
		help='Find timeseries that are current'
	)
	group.add_argument(
		'--not-current',
		dest='current',
		action='store_false',
		help='Find timeseries that are not current'
	)

	parser.add_argument(
		'--start-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find timeseries containing data after the provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--end-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find timeseries containing data before the provided date (ISO8601 format)'
	)

	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		organization=args.organization,
		name=args.name,
		type=args.type,
		current=args.current,
		start=args.start_date,
		end=args.end_date,
		offset=args.skip,
		limit=args.limit
	)
