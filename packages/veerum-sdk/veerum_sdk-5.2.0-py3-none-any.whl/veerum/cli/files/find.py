from datetime import datetime
from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for files'
	)
	parser.set_defaults(command=main, uploaded=None)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find files attached to a workscope'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find files attached to an organization'
	)

	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='Find files with a matching name'
	)
	parser.add_argument(
		'-m',
		'--mimetype',
		default=None,
		help='Find files with a matching mimetype'
	)
	parser.add_argument(
		'--start-date',
		default = None,
		type = datetime.fromisoformat,
		help = 'Find files after the provided date (ISO8601 format)'
	)
	parser.add_argument(
		'--end-date',
		default = None,
		type = datetime.fromisoformat,
		help = 'Find files before the provided date (ISO8601 format)'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'--uploaded',
		dest='uploaded',
		action='store_const',
		const=1,
		help='Find files that have been uploaded'
	)
	group.add_argument(
		'--not-uploaded',
		dest='uploaded',
		action='store_const',
		const=0,
		help='Find files that have not been uploaded yet'
	)

	supports_sorting(parser, 'name', 'size')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		organization=args.organization,
		name=args.name,
		mimetype=args.mimetype,
		uploaded=args.uploaded,
		start=args.start_date,
		end=args.end_date,
		sort=args.sort,
		order=args.order,
		offset=args.skip,
		limit=args.limit
	)
