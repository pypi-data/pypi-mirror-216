def supports_pagination(parser):
	parser.add_argument(
		'-s',
		'--skip',
		type=int,
		default=None,
		help='Offset into the returned records (default: 0)'
	)
	parser.add_argument(
		'-l',
		'--limit',
		type=int,
		default=None,
		help='Maximum number of records to return (default: 10, maximum: 1000)'
	)

def supports_sorting(parser, *fields):
	parser.add_argument(
		'--sort',
		choices=fields,
		default=None,
		help='Field to sort results by'
	)

	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'--asc',
		dest='order',
		action='store_const',
		const=1,
		default=None,
		help='Results in ascending order'
	)
	group.add_argument(
		'--desc',
		dest='order',
		action='store_const',
		const=-1,
		default=None,
		help='Results in descending order'
	)