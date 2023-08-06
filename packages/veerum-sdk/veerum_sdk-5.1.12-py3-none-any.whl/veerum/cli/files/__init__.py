from . import find
from . import inspect
from . import update
from . import delete
from . import upload
from . import download

from ...sdk import Files

def add_arguments(subparser):
	parser = subparser.add_parser(
		'files',
		description='File access and management utilties',
	)
	parser.set_defaults(client_class=Files)

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
		download
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
