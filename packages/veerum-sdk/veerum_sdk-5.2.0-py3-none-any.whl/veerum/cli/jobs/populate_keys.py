def add_arguments(subparser):
	parser = subparser.add_parser(
		'populate_keys',
		description='Sync the object keys between objects and object_keys collection for the quick access from UI app.'
	)
	parser.set_defaults(command=main)

async def main(args):
	return await args.client.populate_keys()
