from . import wms_shared
from .. import integrations_shared

def add_arguments(subparser):
	parser = subparser.add_parser(
		'create',
		description='Create a new integration'
	)
	parser.set_defaults(command=main)
	integrations_shared.arg_org(parser, 'create')
	wms_shared.add_args(parser)

async def main(args):
	return await args.client.wms_integration(
		args.organization,
		args.endpoint,
		args.layers
	)
