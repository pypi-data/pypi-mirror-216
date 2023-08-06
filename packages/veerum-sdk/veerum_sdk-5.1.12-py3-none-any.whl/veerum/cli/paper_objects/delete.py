def add_arguments(subparser):
    parser = subparser.add_parser(
		'delete',
		description='Delete paper objects'
	)

    parser.set_defaults(command=main)

    parser.add_argument(
		'-po',
		'--paperObject',
		help='Existing paper Object'
	)

async def main(args):
    print('deleting...')
    try:
        await args.client.delete(args.paperObject)
    except:
        return('failed')
    return('success')
