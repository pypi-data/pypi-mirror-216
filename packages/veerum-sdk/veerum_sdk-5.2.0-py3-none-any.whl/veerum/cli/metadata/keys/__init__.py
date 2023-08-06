from . import add
from . import clear
from . import find
from . import set


def add_arguments(subparser):
	parser = subparser.add_parser(
		'keys',
		description='Metadata key management'
	)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands'
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		add,
		clear,
		find,
		set,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
