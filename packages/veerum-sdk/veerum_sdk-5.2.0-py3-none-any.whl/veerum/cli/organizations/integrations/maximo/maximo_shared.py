def arg_endpoint(parser):
	parser.add_argument(
		'-e',
		'--endpoint',
		required=True,
		help='Maximo endpoint'
	)

def arg_apikey(parser):
	parser.add_argument(
		'-k',
		'--apikey',
		help='Maximo api key'
	)

def add_args(parser):
	arg_endpoint(parser)
	arg_apikey(parser)
