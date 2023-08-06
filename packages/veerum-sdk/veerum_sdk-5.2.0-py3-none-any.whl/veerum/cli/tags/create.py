def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a tag'
	)
	parser.set_defaults(command=main, current=False)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='ID of the workscope this tag should be attached to'
	)
	parser.add_argument(
		'-n',
		'--name',
		required=True,
		help='Possible name'
	)
	parser.add_argument(
		'-v',
		'--values',
		required=True,
		help='Comma separated values',
	)
	parser.add_argument(
		'-c',
		'--colors',
		required=False,
		help='Comma separated values',
	)

async def main(args):
	return await args.client.create(
		workscope=args.workscope,
		name=args.name,
		values=args.values,
		colors=args.colors,
	)
