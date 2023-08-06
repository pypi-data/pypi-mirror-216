from . import find
from . import inspect
from . import delete

from ...sdk import Annotations

def add_arguments(subparser):
	parser = subparser.add_parser(
		'annotations',
		description='Annotation access and management utilties',
	)
	parser.set_defaults(client_class=Annotations)

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
		delete,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
