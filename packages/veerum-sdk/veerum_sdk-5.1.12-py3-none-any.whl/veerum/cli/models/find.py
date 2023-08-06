from datetime import datetime
from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for models'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find models attached to a workscope'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find models attached to an organization'
	)
	parser.add_argument(
		'--format',
		choices=['potree', 'unity', 'draco'],
		default=None,
		help='Find models by format'
	)
	parser.add_argument(
		'--type',
		choices=['actual', 'design', 'computed'],
		default=None,
		help='Find models by type'
	)
	parser.add_argument(
		'--start-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find models created after provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--end-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find models created before provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--category',
		default=None,
		help='Find models by category'
	)

	supports_sorting(parser, 'name', 'date')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		organization=args.organization,
		format=args.format,
		type=args.type,
		start=args.start_date,
		end=args.end_date,
		offset=args.skip,
		limit=args.limit,
		category=args.category
	)
