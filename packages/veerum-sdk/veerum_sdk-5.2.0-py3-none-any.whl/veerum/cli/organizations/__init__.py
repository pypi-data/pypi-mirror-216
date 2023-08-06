from . import create
from . import find
from . import inspect
from . import update
from . import delete
from . import integrations
from ...sdk import Organizations

def add_arguments(subparser):
	parser = subparser.add_parser(
		'organizations',
		description='Organization access and management utilties'
	)
	parser.set_defaults(client_class=Organizations)

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
		inspect,
		update,
		delete,
		integrations
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
