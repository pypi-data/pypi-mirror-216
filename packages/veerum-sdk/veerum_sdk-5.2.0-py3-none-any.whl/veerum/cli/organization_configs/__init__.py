from . import inspect
from . import update
from ...sdk import OrganizationConfigs

def add_arguments(subparser):
	parser = subparser.add_parser(
		'organization_configs',
		description='Organization config access and management utilties'
	)
	parser.set_defaults(client_class=OrganizationConfigs)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		update,
		inspect,
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)
