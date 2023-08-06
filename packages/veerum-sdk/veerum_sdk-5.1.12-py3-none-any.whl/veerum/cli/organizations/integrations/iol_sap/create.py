from .. import integrations_shared

def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a new IOL SAP integration'
	)
	parser.set_defaults(command=main)

	integrations_shared.arg_org(parser, 'create')
	integrations_shared.arg_cron(parser)

async def main(args):
	return await args.client.iol_sap_integration(
		args.organization,
		args.cron
	)
