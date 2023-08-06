from . import sync
from . import relationship

from ...sdk import Automations


def add_arguments(subparser):
		parser = subparser.add_parser(
			'automations',
			description='Automation management utilties'
    )
		parser.set_defaults(client_class=Automations)

		subparser = parser.add_subparsers(
				title='Sub-commands',
				description='Available sub-commands',
				dest='subcommand',
		)
		# Work around https://bugs.python.org/issue9253
		subparser.required = True

		utilities = [
				sync,
				relationship
		]

		for utility in utilities:
				if (hasattr(utility, 'add_arguments')):
						utility.add_arguments(subparser)
