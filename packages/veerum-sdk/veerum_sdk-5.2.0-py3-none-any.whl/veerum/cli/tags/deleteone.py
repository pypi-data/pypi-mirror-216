def add_arguments(subparser):
    parser = subparser.add_parser(
        'deleteone',
        description='Delete a tag by ID'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-t',
        '--tag',
        required=True,
        help='ID of tag to remove'
    )


async def main(args):
    return await args.client.deleteOne(args.tag)
