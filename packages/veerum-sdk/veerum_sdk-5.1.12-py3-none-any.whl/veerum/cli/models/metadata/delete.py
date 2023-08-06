def add_arguments(subparser):
  parser = subparser.add_parser(
    'delete',
    description='Remove metadata from a model',
  )
  parser.set_defaults(command=main)

  parser.add_argument(
    '-m',
    '--model',
    required=True,
    help='Model the metadata should be deleted from'
  )

async def main(args):
  return await args.client.delete_metadata(
    args.model
  )
