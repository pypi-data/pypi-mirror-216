from . import create
from . import ingest
from . import delete
from . import find
from . import update
from . import inspect
from . import delete_many

from ...sdk import PaperObjects


def add_arguments(subparser):
		parser = subparser.add_parser(
			'paper_objects',
			description='Paper Object management utilties'
    )
		parser.set_defaults(client_class=PaperObjects)

		subparser = parser.add_subparsers(
				title='Sub-commands',
				description='Available sub-commands',
				dest='subcommand',
		)
		# Work around https://bugs.python.org/issue9253
		subparser.required = True

		utilities = [
				create,
				find,
				ingest,
				delete,
				update,
				inspect,
        delete_many
		]

		for utility in utilities:
				if (hasattr(utility, 'add_arguments')):
						utility.add_arguments(subparser)
