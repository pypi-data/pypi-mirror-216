from datetime import datetime

from .. import retcode

def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Update a milestone'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-m',
		'--milestone',
		dest='milestone',
		required=True,
		help='ID of milestone to modify'
	)

	parser.add_argument(
		'-w',
		'--workscope',
		default=None,
		help='ID of the workscope this milestone should be attached to'
	)
	parser.add_argument(
		'-d',
		'--date',
		default=None,
		type=datetime.fromisoformat,
		help='Date of the milestone (ISO8601 format)'
	)
	parser.add_argument(
		'-l',
		'--label',
		default=None,
		help='Displayed name of the milestone'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'--critical',
		default=None,
		dest='critical',
		action='store_true',
		help='Mark this milestone as critical'
	)
	group.add_argument(
		'--not-critical',
		default=None,
		dest='critical',
		action='store_false',
		help='Mark this milestone as not critical'
	)

	parser.add_argument(
		'-s',
		'--source',
		default=None
	)
	parser.add_argument(
		'-t',
		'--target',
		type=float,
		default=None,
	)

	parser.add_argument(
		'--line-color',
		dest='line_color',
		default=None,
		help='A hex color (e.g. #000000)',
	)
	parser.add_argument(
		'--lineWidth',
		dest='line_width',
		default=None,
		help='Thickness of the vertical line in the rendered chart. Must be >= 0.',
	)

async def main(args):
	return await args.client.update(
		args.milestone,
		workscope=args.workscope,
		date=args.date,
		label=args.label,
		critical=args.critical,
		source=args.source,
		target=args.target,
		line_color=args.line_color,
		line_width=args.line_width,
	)
