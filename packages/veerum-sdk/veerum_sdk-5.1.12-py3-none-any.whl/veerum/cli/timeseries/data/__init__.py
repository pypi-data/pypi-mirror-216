from . import add
from . import clear
from . import delete
from . import get
from . import set

def add_arguments(subparser):
	parser = subparser.add_parser(
		'data',
		description='Timeseries data management'
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
		delete,
		get,
		set,
	]

	for utility in utilities:
		if(hasattr(utility, 'add_arguments')):
			utility.add_arguments(subparser)
