def add_arguments(subparser):
	parser = subparser.add_parser(
		'ls',
		description='Search for keys'
	)
	parser.set_defaults(command=main)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'-m',
		'--model',
		default=None,
		help='List keys used by a model\'s metadata'
	)
	group.add_argument(
		'-o',
		'--organization',
		default=None,
		help='List keys used by and organization'
	)


async def main(args):
	if args.model is None:
		return await args.client.all_keys(args.organization)
	else:
		return await args.client.get_keys(args.model)
