def add_arguments(subparser):
		parser = subparser.add_parser(
				'sync',
				description='Sync paper Objects and 3D objects'
		)
		parser.set_defaults(command=main)
		parser.add_argument(
				'-w',
				'--workscope',
				required=True,
				help='ID of the Workscope to be search (Required)'
		)
		parser.add_argument(
				'-m',
				'--model',
				help='ID of the Model to be search'
		)
		parser.add_argument(
				'-s',
				'--search_field',
				required=True,
				help='Search Field (Required)'
		)

async def main(args):

		return await args.client.sync(
				workscope=args.workscope,
				search_field=args.search_field,
				model=args.model if args.model else None
		)
