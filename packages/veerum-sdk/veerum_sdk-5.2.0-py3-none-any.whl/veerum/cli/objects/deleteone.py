def add_arguments(subparser):
    parser = subparser.add_parser(
        'deleteone',
        description='Delete an object by ID'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-o',
        '--object',
        required=True,
        help='ID of object to remove'
    )


async def main(args):
    return await args.client.deleteOne(args.object)
