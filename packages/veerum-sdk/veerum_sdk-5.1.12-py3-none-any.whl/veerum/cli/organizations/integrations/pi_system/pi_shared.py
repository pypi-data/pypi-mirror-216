def arg_endpoint(parser):
	parser.add_argument(
		'-e',
		'--endpoint',
		required=True,
		help='PI System endpoint'
	)

def arg_username(parser):
	parser.add_argument(
		'-u',
		'--username',
		help='PI System windows username'
	)

def arg_password(parser):
	parser.add_argument(
		'-p',
		'--userpassword',
		help='PI System windows user password'
	)

def arg_assetservername(parser):
	parser.add_argument(
		'-asn',
		'--assetservername',
		help='PI System asset server name'
	)

def arg_assetdatabasename(parser):
	parser.add_argument(
		'-adn',
		'--assetdatabasename',
		help='PI System asset database name'
	)

def add_args(parser):
	arg_endpoint(parser)
	arg_username(parser)
	arg_password(parser)
	arg_assetservername(parser)
	arg_assetdatabasename(parser)
