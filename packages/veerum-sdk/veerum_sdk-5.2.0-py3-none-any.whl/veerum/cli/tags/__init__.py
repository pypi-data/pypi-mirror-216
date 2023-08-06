from . import create
from . import update
from . import find
from . import delete
from . import deleteone

from ...sdk import Tags

def add_arguments(subparser):
	parser = subparser.add_parser(
		'status',
		description='Object Status access and management'
	)
	parser.set_defaults(client_class=Tags)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)

	subparser.required = True

	utilities = [ 
		create,
		update,
		find,
		delete,
		deleteone,
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
