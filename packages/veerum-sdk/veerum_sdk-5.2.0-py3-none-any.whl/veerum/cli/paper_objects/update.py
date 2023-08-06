def add_arguments(subparser):
		parser = subparser.add_parser(
				'update',
				description='Update an existing paper object'
		)
		parser.set_defaults(command=main)

		parser.add_argument(
				'-po',
				'--paperObject',
				required=True,
				help='ID of paper object to Update'
		)		

		parser.add_argument(
				'-o',
				'--object',
				help='ID of object to attach to paper object'
		)

		parser.add_argument(
				'-t',
				'--text',
				required=False,
				help='name of the paper Object'
		)

		parser.add_argument(
			'-b',
			'--bbox',
			required=False,
			help='Comma separated values ex. 13,2,3',
		)

		parser.add_argument(
				'-p',
				'--page',
				required=False,
				help='Page # in the file of the paper Object'
		)

		parser.add_argument(
			'-c',
			'--color',
			required=False,
			help='Hex value ex. #fffff (string)',
		)


async def main(args):
	return await args.client.update(
			paperObject=args.paperObject,
			object=args.object if args.object else None,
			text=args.text if args.text else None,
			bbox=args.bbox.split(',') if args.bbox else None,
			color=args.color if args.color else None,
			page=args.page if args.page else None,
		)
