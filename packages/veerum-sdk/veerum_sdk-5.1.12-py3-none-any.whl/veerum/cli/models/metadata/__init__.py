from . import set
from . import delete

def add_arguments(subparser):
  parser = subparser.add_parser(
    'metadata',
    description='Utilities to configure model metadata'
  )

  subparser = parser.add_subparsers(
    title='Sub-commands',
    description='Available sub-commands',
    dest='subcommand',
  )
  subparser.required = True

  utilities = [
    set,
    delete
  ]

  for utility in utilities:
    if(hasattr(utility, 'add_arguments')):
      utility.add_arguments(subparser)
