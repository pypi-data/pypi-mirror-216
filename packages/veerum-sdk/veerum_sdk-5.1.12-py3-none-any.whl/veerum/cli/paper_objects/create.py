def add_arguments(subparser):
		parser = subparser.add_parser(
				'create',
				description='Create a new workscope'
		)
		parser.set_defaults(command=main)

		parser.add_argument(
				'-t',
				'--text',
				required=True,
				help='name of the paper Object (Required)'
		)

		parser.add_argument(
			'-b',
			'--bbox',
			required=True,
			help='Comma separated values ex. 13,2,3',
		)

		parser.add_argument(
				'-p',
				'--page',
				required=True,
				help='Page # in the file of the paper Object (Required)'
		)

		parser.add_argument(
			'-c',
			'--color',
			required=False,
			help='Hex value ex. #fffff (string)',
		)

		parser.add_argument(
				'-org',
				'--organization',
				required=True,
				help='ID of the Organization this paper object should be attached to (Required)'
		)

		parser.add_argument(
				'-w',
				'--workscope',
				required=True,
				help='ID of the Workscope this paper object should be attached to (Required)'
		)
		
		parser.add_argument(
				'-obj',
				'--object',
				required=True,
				help='ID of the Object this paper object should be attached to (Required)'
		)
		
		parser.add_argument(
				'-f',
				'--file',
				required=True,
				help='ID of the file this paper object should be attached to (Required)'
		)

async def main(args):

		return await args.client.create(
				organization=args.organization,
				workscope=args.workscope,
				object=args.object,
				file=args.file,
				text=args.text,
				bbox=args.bbox.split(','),
				color=args.color if args.color else None,
				page=args.page,
		)
