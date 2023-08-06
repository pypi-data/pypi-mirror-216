from . import find
from . import create
from . import inspect
from . import update
from . import tags
from . import features
from . import delete

from ...sdk import Workscopes

def add_arguments(subparser):
	parser = subparser.add_parser(
		'workscopes',
		description='Work scope access and management utilties'
	)
	parser.set_defaults(client_class=Workscopes)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		find,
		create,
		inspect,
		update,
		tags,
		features,
		delete,
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
