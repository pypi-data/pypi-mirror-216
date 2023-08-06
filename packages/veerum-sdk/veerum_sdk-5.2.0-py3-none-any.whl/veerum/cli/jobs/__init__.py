from . import warn_inactive_users
from . import populate_keys
from . import misplaced_objects

from ...sdk import Jobs

def add_arguments(subparser):
	parser = subparser.add_parser(
		'jobs',
		description='Run a cron job'
	)
	parser.set_defaults(client_class=Jobs)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [ 
		warn_inactive_users,
		populate_keys,
    misplaced_objects,
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
