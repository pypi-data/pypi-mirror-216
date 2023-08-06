def add_arguments(subparser):
		parser = subparser.add_parser(
		'delete_many',
		description='Delete paper objects'
	)

		parser.set_defaults(command=main)
		
		parser.add_argument(
		'-f',
		'--file',
		help='Linked File ID'
	)
		parser.add_argument(
		'-o',
		'--object',
		help='Linked Object ID'
	)

async def main(args):
		print('deleting...')
		try:
				await args.client.delete_many(
					file=args.file if args.file else None,
					object=args.object if args.object else None
				)
		except:
				return('failed')
		return('success')
