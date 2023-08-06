from . import integrations_shared

def add_arguments(subparser):
	parser = subparser.add_parser(
		'rm',
		description='Delete an integration'
	)
	parser.set_defaults(command=main)

	integrations_shared.arg_org(parser)
	integrations_shared.arg_integration_id(parser)

async def main(args):
	return await args.client.delete_integration(
		args.organization,
		args.integration
	)
