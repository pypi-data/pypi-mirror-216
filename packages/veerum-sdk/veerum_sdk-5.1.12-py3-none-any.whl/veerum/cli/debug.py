from ..sdk.base import BaseClient
import os

def add_arguments(subparser):
	parser = subparser.add_parser(
		'debug',
		description='info to help debugging issues'
	)
	parser.set_defaults(client_class=BaseClient, command=main)

async def main(args):
	USER_PATH = os.path.expanduser(os.path.join('~'))
	return {
		"user_path": USER_PATH
	}