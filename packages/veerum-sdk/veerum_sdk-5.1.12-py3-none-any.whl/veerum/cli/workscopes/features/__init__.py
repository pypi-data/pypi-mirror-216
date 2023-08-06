from . import add
from . import remove

def add_arguments(subparser):
	parser = subparser.add_parser(
		'features',
		description='Workscope feature management'
	)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands'
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		add,
		remove,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
