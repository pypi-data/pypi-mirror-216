from . import find
from . import inspect
from . import update
from . import delete
from . import upload
from . import download
from . import metadata

from ...sdk import Models

def add_arguments(subparser):
	parser = subparser.add_parser(
		'models',
		description='Model access and management utilties'
	)
	parser.set_defaults(client_class=Models)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		find,
		inspect,
		update,
		delete,
		upload,
		download,
		metadata
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
