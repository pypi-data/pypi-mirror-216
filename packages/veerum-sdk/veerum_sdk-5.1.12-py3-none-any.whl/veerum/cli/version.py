import pkg_resources

try:
    __version__ = pkg_resources.get_distribution('veerum-sdk').version
except Exception:
    __version__ = 'unknown'

from ..sdk.base import BaseClient

def add_arguments(subparser):
	parser = subparser.add_parser(
		'version',
		description='Inspect a file'
	)
	parser.set_defaults(client_class=BaseClient, command=main)

async def main(args):
	try:
		api = await args.client.status()
	except:
		api = {}

	return {
		"cli": __version__
		# "api": api.get('version', 'unknown'),
	}
