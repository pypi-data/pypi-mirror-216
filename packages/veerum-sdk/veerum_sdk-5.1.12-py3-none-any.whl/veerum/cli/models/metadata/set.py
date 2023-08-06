import os
import json

def add_arguments(subparser):
  parser = subparser.add_parser(
    'set',
    description='Pass a json file that will be set as the model\'s metadata',
  )
  parser.set_defaults(command=main)

  parser.add_argument(
    '-m',
    '--model',
    required=True,
    help='Model the metadata should be associated with'
  )

  parser.add_argument('path', help='Path to json file of metadata')

async def main(args):
  jsonPath = os.path.normpath(args.path)
  with open(jsonPath) as json_file:
    parsed_json = json.load(json_file)

    return await args.client.set_metadata(
      args.model,
      parsed_json
    )
