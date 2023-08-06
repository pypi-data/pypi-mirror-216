def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a timeseries'
	)
	parser.set_defaults(command=main, current=False)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='ID of the workscope this timeseries should be attached to'
	)
	parser.add_argument(
		'--x-unit',
		required=True,
		help='Units for the x-axis'
	)
	parser.add_argument(
		'--y-unit',
		required=True,
		help='Units for the y-axis'
	)
	parser.add_argument(
		'--x-label',
		default=None,
		help='Label for the x-axis'
	)
	parser.add_argument(
		'--y-label',
		required=True,
		help='Label for the y-axis'
	)

	parser.add_argument(
		'--current',
		dest='current',
		action='store_true',
		help='Indicates that this timeseries is the most recent and displays it from the UI'
	)
	parser.add_argument(
		'--not-current',
		dest='current',
		action='store_false',
		help='Indicates that this timeseries is not the most recent and hides it from the UI'
	)

	parser.add_argument(
		'-n',
		'--name',
		default=None,
	)
	parser.add_argument(
		'--type',
		required=True,
	)

	parser.add_argument(
		'--point-style',
		dest='point_style',
		default=None,
		choices=['circle', 'cross', 'crossRot', 'dash', 'line', 'rect', 'rectRounded', 'rectRot', 'star', 'triangle'],
		help='How to style the points in the rendered chart'
	)
	parser.add_argument(
		'--point-color',
		dest='point_color',
		default=None,
		help='A hex color (e.g. #000000)',
	)
	parser.add_argument(
		'--chart-radius',
		dest='chart_radius',
		type=float,
		default=None,
		help='The size of the graph points in the rendered chart. Must be >= 0.',
	)

async def main(args):
	return await args.client.create(
		workscope=args.workscope,
		x_unit=args.x_unit,
		y_unit=args.y_unit,
		x_label=args.x_label,
		y_label=args.y_label,
		current=args.current,
		name=args.name,
		type=args.type,
		point_style=args.point_style,
		point_color=args.point_color,
		chart_radius=args.chart_radius,
	)
