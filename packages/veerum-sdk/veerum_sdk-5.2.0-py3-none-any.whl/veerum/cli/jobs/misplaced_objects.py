def add_arguments(subparser):
	parser = subparser.add_parser(
		'misplaced_objects',
		description='Create report on datadog about the misplaced objects.'
	)
	parser.set_defaults(command=main)

async def main(args):
	return await args.client.misplaced_objects()
