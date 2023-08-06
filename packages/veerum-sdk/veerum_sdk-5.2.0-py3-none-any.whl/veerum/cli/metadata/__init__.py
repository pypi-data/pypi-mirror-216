from . import upload
from . import keys
from . import inspect
from . import find

from ...sdk import Metadata

def add_arguments(subparser):
	parser = subparser.add_parser(
		'metadata',
		description='Metadata management utilties'
	)
	parser.set_defaults(client_class=Metadata)

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
		upload,
		keys
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
