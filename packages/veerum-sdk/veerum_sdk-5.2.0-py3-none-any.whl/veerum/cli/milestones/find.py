from datetime import datetime

from ..common import supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for milestones'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find milestones attached to a workscope'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find milestones attached to an organization'
	)

	parser.add_argument(
		'--start-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find milestones after the provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--end-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find milestones before the provided date (ISO8601 format)'
	)

	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		organization=args.organization,
		start=args.start_date,
		end=args.end_date,
		offset=args.skip,
		limit=args.limit
	)
