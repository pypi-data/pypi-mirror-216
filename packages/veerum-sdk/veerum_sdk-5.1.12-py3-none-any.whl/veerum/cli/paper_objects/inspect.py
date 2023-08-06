def add_arguments(subparser):
    parser = subparser.add_parser(
        'inspect',
        description='Inspect an Paper Object'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-po',
        '--paperObject',
        required=True,
        help='ID of object to inspect'
    )


async def main(args):
    return await args.client.get(args.paperObject)
