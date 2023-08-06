def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for tags'
	)
	parser.set_defaults(command=main)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='List tags used by a workscope'
	)
	group.add_argument(
		'-o',
		'--organization',
		default=None,
		help='List tags used by and organization'
	)

async def main(args):
	if args.workscope is None:
		return await args.client.all_tags(args.organization)
	else:
		return await args.client.get_tags(args.workscope)
