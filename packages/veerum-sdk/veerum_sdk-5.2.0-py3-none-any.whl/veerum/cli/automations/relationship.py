def add_arguments(subparser):
		parser = subparser.add_parser(
				'relationship',
				description='Relate parent 3D objects to childs 3D objects'
		)
		parser.set_defaults(command=main)
		parser.add_argument(
				'-w',
				'--workscope',
				help='ID of the Workscope to be search'
		)
		parser.add_argument(
				'-m',
				'--model',
				help='ID of the Model to be search'
		)

async def main(args):

		return await args.client.relationship(
				workscope=args.workscope,
				model=args.model if args.model else None
		)
