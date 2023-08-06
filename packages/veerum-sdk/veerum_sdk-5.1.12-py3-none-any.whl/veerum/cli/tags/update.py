def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Update a tag'
	)
	parser.set_defaults(command=main, current=False)

	parser.add_argument(
		'-t',
		'--tag',
		required=True,
		help='ID of tag to update'
  )

	parser.add_argument(
		'-n',
		'--name',
		help='Possible name'
	)
	parser.add_argument(
		'-v',
		'--values',
		help='Comma separated values',
	)
	parser.add_argument(
		'-c',
		'--colors',
		help='Comma separated values',
	)

async def main(args):
	return await args.client.update(
		name=args.name,
		values=args.values,
		tag=args.tag,
		colors=args.colors,
	)
