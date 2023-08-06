from . import delete
from . import find
from . import wms
from . import pi_system
from . import watson_ir
from . import maximo
from . import iol_sap

def add_arguments(subparser):
	parser = subparser.add_parser(
		'integrations',
		description='Organization integrations management'
	)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand'
	)

	subparser.required = True

	utilities = [
		delete,
		find,
		wms,
    pi_system,
    watson_ir,
		maximo,
		iol_sap
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
