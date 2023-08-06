from .. import integrations_shared

def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Updates an integration'
	)
	parser.set_defaults(command=main)

	integrations_shared.arg_org(parser)
	integrations_shared.arg_integration_id(parser)
	integrations_shared.arg_cron(parser)

async def main(args):
	return await args.client.watson_ir_integration(
		args.organization,
		args.cron,
		integration=args.integration
	)
