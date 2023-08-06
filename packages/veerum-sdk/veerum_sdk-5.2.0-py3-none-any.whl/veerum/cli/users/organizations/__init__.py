from . import find
from . import join
from . import leave

def add_arguments(subparser):
	parser = subparser.add_parser(
		'organizations',
		description='User organization membership management'
	)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		find,
		join,
		leave,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
