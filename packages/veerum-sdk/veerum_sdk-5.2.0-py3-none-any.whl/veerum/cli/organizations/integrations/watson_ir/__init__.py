from . import create
from . import update

def add_arguments(subparser):
	parser = subparser.add_parser(
		'watson_ir',
		description='Organization integrations pi_system'
	)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand'
	)

	subparser.required = True

	utilities = [
		create,
		update
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
