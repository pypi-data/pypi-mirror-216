from datetime import datetime

from ..common import supports_sorting, supports_pagination


def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for metadata'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--model',
		default=None,
		help='Find metadata attached to a model'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find metadata attached to an organization'
	)
	parser.add_argument(
		'--start-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find metadata created after provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--end-date',
		default=None,
		type=datetime.fromisoformat,
		help='Find metadata created before provided date (ISO8601 format)'
	)

	supports_sorting(parser, 'name', 'date')
	supports_pagination(parser)


async def main(args):
	return await args.client.find(
		model=args.model,
		organization=args.organization,
		start=args.start_date,
		end=args.end_date,
		offset=args.skip,
		limit=args.limit
	)
