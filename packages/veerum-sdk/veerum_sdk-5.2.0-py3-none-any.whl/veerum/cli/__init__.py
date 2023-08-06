import sys
import json
import logging
import argparse

from getpass import getpass
from functools import partial

from tornado import ioloop

from . import files
from . import jobs
from . import milestones
from . import organizations
from . import models
from . import timeseries
from . import users
from . import workbreakdowns
from . import workscopes
from . import annotations
from . import metadata
from . import objects
from . import version
from . import debug
from . import tags
from . import paper_objects
from . import automations
from . import organization_configs

from . import retcode
from ..sdk import base

from backports.datetime_fromisoformat import MonkeyPatch

# Make sure datetime.fromisoformat is available in earlier python versions
MonkeyPatch.patch_fromisoformat()

TOKEN_REGENERATION_RATE = 3600

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s - %(message)s")
logging.getLogger('py.warnings').setLevel(logging.ERROR)
logging.captureWarnings(True)

async def not_implemented(args):
	print('This feature does not appear to be implemeted yet!', file=sys.stderr)
	return retcode.NOT_IMPLEMENTED

# number of retry attempts for the request if it is returning Bad Gateway (502) result
def attempts_type(a):
	a = int(a)
	if a < 1:
		raise argparse.ArgumentTypeError("Minimum amount of attempts is 1")
	if a > 10:
		raise argparse.ArgumentTypeError("Maximum amount of attempts is 10")
	return a

def get_cli_arguments():
	parser = argparse.ArgumentParser(
		description='The Veerum Command Line Interface is a unified way to manage your Veerum services.'
	)

	# TODO: {KL} Figure out how we are pulling in credentials
	parser.add_argument(
		'--email',
		default=None,
		help='E-mail to use to authenticate with the Veerum API'
	)
	parser.add_argument(
		'--password',
		default=False,
		action='store_true',
		help='Set the password to authenticate with the Veerum API using an interactive password prompt'
	)
	parser.add_argument(
		'--profile',
		default=base.DEFAULT_PROFILE,
		help='Name of the configuration section in ~/.veerum./config to use (Default: %s)' % base.DEFAULT_PROFILE
	)
	parser.add_argument(
		'--endpoint',
		default=None,
		help='URL of the endpoint for making requets'
	)
	parser.add_argument(
		'--attempts',
		type=attempts_type,
		default=5, # applies to all commands
		help='Number of retry attempts to get API results'
	)
	parser.add_argument(
		'--sleep',
		type=float,
		default=1, # applies to all commands
		help='Number of seconds between retry attempts'
	)

	parser.set_defaults(command=not_implemented)

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		dest='subcommand',
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		files,
		milestones,
		organizations,
		models,
		timeseries,
		users,
		workbreakdowns,
		workscopes,
		annotations,
		metadata,
		objects,
		version,
		debug,
		jobs,
		tags,
		paper_objects,
		automations,
		organization_configs
	]

	for utility in utilities:
		if hasattr(utility, 'add_arguments'):
			utility.add_arguments(subparser)

	return parser.parse_args()

async def generate_token(client):
	response = await client.login()
	if response is None:
		raise Exception('Authentication Failed')

	token = response.get('accessToken', None)
	if token is None:
		raise Exception('Authentication Failed')

	client.set_token(token)

async def regenerate_token(client, period=None):
	try:
		await generate_token(client)
		logging.debug('Regenerated authentication token')
	except Exception as ex:
		logging.exception(ex)
		logging.error('Failed to regenerate authentication token')

	if not period is None:
		ioloop.IOLoop.current().call_later(
			period,
			regenerate_token,
			client,
			period=period
		)

async def __entry_point(args):
	args.password = getpass() if args.password else None

	client_config = {
		'profile': args.profile,
		'email': args.email,
		'password': args.password,
		# TODO: {KL} This will need to be changed when we get a backend SSL cert working
		'force_ssl': False,
		# retry functionality
		'attempts': args.attempts,
		'sleep': args.sleep
	}
	try:
		client = args.client_class(**client_config)
	except Exception as ex:
		logging.error(ex)
		return retcode.CONFIGURATION_ERROR

	try:
		await generate_token(client)
	except Exception as ex:
		logging.error(ex)
		return retcode.AUTHENTICATION_FAILED

	# Periodically regenerate the login token so long running tasks do not fail
	ioloop.IOLoop.current().call_later(
		TOKEN_REGENERATION_RATE,
		regenerate_token,
		client,
		period=TOKEN_REGENERATION_RATE
	)

	setattr(args, 'client', client)

	try:
		return await args.command(args)
	except Exception as ex:
		# TODO: {KL} This should never happen
		logging.exception(ex)
		return retcode.GENERAL_ERROR

def main():
	args = get_cli_arguments()
	result = ioloop.IOLoop.current().run_sync(partial(__entry_point, args))

	if isinstance(result, int):
		exit(result)

	print(json.dumps(result, sort_keys=True, indent=2))
	exit(retcode.OK)

if __name__ == '__main__':
	main()
