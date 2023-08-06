from . import find
from . import inspect
from . import create
from . import update
from . import delete

from ...sdk import Milestones

def add_arguments(subparser):
	parser = subparser.add_parser(
		'milestones',
		description='Milestone access and management utilties'
	)
	parser.set_defaults(client_class=Milestones)

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
		create,
		update,
		delete,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
