from . import maximo_shared
from .. import integrations_shared

def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Updates a Maximo integration'
	)
	parser.set_defaults(command=main)

	integrations_shared.arg_org(parser)
	integrations_shared.arg_integration_id(parser)
	integrations_shared.arg_cron(parser)
	maximo_shared.add_args(parser)

async def main(args):
	return await args.client.maximo_integration(
		args.organization,
		args.cron,
		args.endpoint,
		args.apikey,
		integration=args.integration
	)
