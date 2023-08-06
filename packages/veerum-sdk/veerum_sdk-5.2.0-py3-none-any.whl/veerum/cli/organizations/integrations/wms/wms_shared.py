def arg_endpoint(parser):
	parser.add_argument(
		'-e',
		'--endpoint',
		required=True,
		help='WMS endpoint'
	)
	
def arg_layers(parser):
	parser.add_argument(
		'-l',
		'--layers',
		required=True,
		nargs='+',
		help='Array of WMS layers'
	)

def add_args(parser):
	arg_endpoint(parser)
	arg_layers(parser)
