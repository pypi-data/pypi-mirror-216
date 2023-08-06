from . import ingest
from . import delete
from . import find
from . import update
from . import inspect
from . import deleteone
from . import upload

from ...sdk import Objects


def add_arguments(subparser):
    parser = subparser.add_parser(
        'objects',
        description='Object management utilties'
    )
    parser.set_defaults(client_class=Objects)

    subparser = parser.add_subparsers(
        title='Sub-commands',
        description='Available sub-commands',
        dest='subcommand',
    )
    # Work around https://bugs.python.org/issue9253
    subparser.required = True

    utilities = [
        find,
        ingest,
        delete,
        update,
        inspect,
        deleteone,
        upload
    ]

    for utility in utilities:
        if (hasattr(utility, 'add_arguments')):
            utility.add_arguments(subparser)
