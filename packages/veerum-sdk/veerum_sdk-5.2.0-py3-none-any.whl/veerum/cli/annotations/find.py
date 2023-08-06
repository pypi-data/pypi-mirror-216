from ..common import supports_sorting, supports_pagination

def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for annotations'
	)
	parser.set_defaults(command=main, resolved=None)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='Find annotations attached to a workscope'
	)
	parser.add_argument(
		'-o',
		'--organization',
		default=None,
		help='Find annotations attached to an organization'
	)

	parser.add_argument(
		'-t',
		'--title',
		default=None,
		help='Find annotations with a matching title'
	)
	parser.add_argument(
		'-c',
		'--comment',
		default=None,
		help='Find annotations with a matching comment'
	)

	parser.add_argument(
		'-d',
		'--deleted',
		default=False,
		help='Find deleted annotations. False by default.'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'--resolved',
		dest='resolved',
		action='store_const',
		const=1,
		help='Find annotations that have been resolved'
	)
	group.add_argument(
		'--not-resolved',
		dest='resolved',
		action='store_const',
		const=0,
		help='Find annotations that have not been resolved yet'
	)

	supports_sorting(parser, 'title')
	supports_pagination(parser)

async def main(args):
	return await args.client.find(
		workscope=args.workscope,
		organization=args.organization,
		title=args.title,
		comment=args.comment,
		resolved=args.resolved,
		sort=args.sort,
		order=args.order,
		offset=args.skip,
		limit=args.limit,
		deleted=args.deleted
	)
