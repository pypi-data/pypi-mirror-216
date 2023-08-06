def add_arguments(subparser):
    parser = subparser.add_parser(
		'delete',
		description='Delete objects and metadata from a model OR workscope'
	)

    parser.set_defaults(command=main)

    parser.add_argument(
		'-m',
		'--model',
		help='Existing model'
	) 

    parser.add_argument(
		'-w',
		'--workscope',
		help='Existing workscope'
	) 

async def main(args):
    print('deleting...')
    try:
        await args.client.delete(
            workscope=args.workscope,
            model=args.model
        )
    except:
        return('failed')
    return('success')
