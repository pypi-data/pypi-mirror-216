from . import find
from . import create
from . import inspect
from . import update
from . import organizations
from . import workscopes

from ...sdk import Users

def add_arguments(subparser):
	parser = subparser.add_parser(
		'users',
		description='User access and management utilties'
	)
	parser.set_defaults(client_class=Users)

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
		organizations,
		workscopes,
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
