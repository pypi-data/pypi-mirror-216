org_create_msg = 'to add the integration to'
org_update_msg = 'the integration belongs to'

def arg_org(parser, mode='update'):
	parser.add_argument(
		'-o',
		'--organization',
		required=True,
		help='ID of organization ' + (org_create_msg if mode == 'create' else org_update_msg)
	)

def arg_cron(parser):
	parser.add_argument(
		'-c',
		'--cron',
		help='Schedule to run integration on',
	)

def arg_integration_id(parser):
	parser.add_argument(
		'-i',
		'--integration',
		required=True,
		help='ID of the integration'
	)
