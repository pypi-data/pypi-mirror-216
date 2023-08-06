from . import pi_shared
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
	pi_shared.add_args(parser)

async def main(args):
	return await args.client.pi_system_integration(
		args.organization,
		args.cron,
		args.endpoint,
		other_data_tuple=(args.username, args.userpassword, args.assetservername, args.assetdatabasename),
		integration=args.integration
	)
