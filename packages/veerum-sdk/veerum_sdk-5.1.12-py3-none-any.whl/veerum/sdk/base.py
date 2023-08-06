import io
import os
import logging
import configparser
import time

from uuid import uuid4
from functools import partial
from datetime import date, datetime
from json import dumps as json_encode
from json import loads as json_decode
from urllib.parse import urlparse, urljoin, urlunparse

from tornado import httpclient
from tornado.escape import url_escape
from tornado.httputil import url_concat, HTTPHeaders

VEERUM_CONFIG_PATH = os.path.join('~', '.veerum', 'config')

# DOCKER = true, when running inside docker container
if 'DOCKER' in os.environ:
	VEERUM_CONFIG_PATH = os.path.join('/run', 'secrets', 'veerum_config')

USER_CONFIG_PATH = os.path.expanduser(VEERUM_CONFIG_PATH)
DEFAULT_PROFILE = 'default'
DEFAULT_USER_AGENT = 'VeerumSDK/0.3.0'
DEFAULT_ENDPOINT = 'http://production.api.local'

DEFAULT_CONFIG = {
	DEFAULT_PROFILE: {
		'user_agent': DEFAULT_USER_AGENT,
	}
}

ENV_VEERUM_EMAIL = 'VEERUM_EMAIL'
ENV_VEERUM_PASSWORD = 'VEERUM_PASSWORD'
ENV_VEERUM_ENDPOINT = 'VEERUM_ENDPOINT'
ENV_VEERUM_USER_AGENT = 'VEERUM_USER_AGENT'

ENVIRONMENT_OVERRIDES = {
	ENV_VEERUM_EMAIL: 'email',
	ENV_VEERUM_PASSWORD: 'password',
	ENV_VEERUM_ENDPOINT: 'endpoint',
	ENV_VEERUM_USER_AGENT: 'user_agent',
}

async def stream_producer(file, write, chunk_size=16384):
	while True:
		chunk = file.read(chunk_size)
		if not chunk:
			break
		await write(chunk)


async def multipart_producer(boundary, files, write):
	boundary_bytes = boundary.encode()

	for file in files:
		filename_bytes = str(file.size).encode()
		filename = file.key.encode()
		buf = (
				(b"--%s\r\n" % boundary_bytes)
				+ (
						b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
						% (filename_bytes, filename)
				)
				+ (b"Content-Type: %s\r\n" % file.mimetype.encode())
				+ b"\r\n"
		)
		await write(buf)
		with open(file.path, "rb") as f:
			while True:
				chunk = f.read(16 * 1024)
				if not chunk:
					break
				await write(chunk)

		await write(b"\r\n")

	await write(b"--%s--\r\n" % (boundary_bytes,))


def update_url(url, **kwargs):
	parsed_url = urlparse(url, scheme='https')
	updated_url = parsed_url._replace(**kwargs)
	return urlunparse(updated_url)


def json_defaults(obj):
	if isinstance(obj, (date, datetime)):
		return obj.isoformat()
	raise TypeError('Object of type %s is not JSON serializable' % type(obj))

def load_configuration_profile(profile=DEFAULT_PROFILE):
	config = configparser.RawConfigParser()

	config.read_dict(DEFAULT_CONFIG)
	config_files = config.read([USER_CONFIG_PATH])

	if not config.has_section(profile):
		raise Exception('Configuration contains no section "{}"'.format(profile))

	for name_env, name_option in ENVIRONMENT_OVERRIDES.items():
		if name_env in os.environ:
			config.set(profile, name_option, os.environ[name_env])

	return config


class BaseClient:
	def __init__(self, profile=DEFAULT_PROFILE, email=None, password=None, endpoint=None, force_ssl=True, verify=True,
				 user_agent=None, attempts=None, sleep=None):
		self.__token = None
		self.__verify = verify

		config = load_configuration_profile(profile=profile)
		patch = {
			'email': email,
			'password': password,
			'endpoint': endpoint,
			'user_agent': user_agent,
		}
		for key, value in patch.items():
			if not value is None:
				config.set(profile, key, value)

		self.endpoint = config.get(profile, 'endpoint', fallback=DEFAULT_ENDPOINT)

		if force_ssl:
			self.endpoint = update_url(self.endpoint, scheme='https')

		self.client = httpclient.AsyncHTTPClient(defaults={
			'user_agent': config.get(profile, 'user_agent', fallback=DEFAULT_USER_AGENT),
			'connect_timeout': 600,
			'request_timeout': 600
		})

		self.__email = config.get(profile, 'email', fallback=None)
		self.__password = config.get(profile, 'password', fallback=None)
		# request retry attempts amount
		self.attempts = attempts
		# seconds between attempts
		self.sleep = sleep

	def join(self, *args):
		return '/'.join((url_escape(el, plus=False) for el in args))

	def pack(self, **kwargs):
		return {k: v for k, v in kwargs.items() if not v is None}

	async def send_request(self, path, method='GET', query={}, headers={}, json=None, body=None, files=None, **kwargs):
		url = urljoin(self.endpoint, path)
		# Remove all empty query parameters
		url = url_concat(url, query)

		headers = HTTPHeaders(headers)

		arguments = {
			'follow_redirects': False,
		}
		arguments.update(
			kwargs,
			method=method,
			headers=headers,
			validate_cert=self.__verify
		)

		if self.__token:
			headers['authorization'] = 'bearer %s' % self.__token

		# TODO: {KL} Throw an error if json and body are both provided
		if not json is None:
			arguments['body'] = json_encode(json, default=json_defaults)
			headers['content-type'] = 'application/json'
		elif isinstance(body, io.IOBase):
			arguments['body_producer'] = partial(stream_producer, body)
		elif files:
			boundary = uuid4().hex
			headers['content-type'] = 'multipart/form-data;boundary=%s' % boundary
			arguments['body_producer'] = partial(multipart_producer, boundary, files)
		else:
			arguments['body'] = body

		request = httpclient.HTTPRequest(url, **arguments)

		for x in range(self.attempts):
			try:
				response = await self.client.fetch(request, raise_error=False)
			except Exception as ex:
				logging.warning(ex)
				raise
			# FIXME: {KL} This is here because reasons
			# Hopefully this is fixed in a future tornado release
			# https://github.com/tornadoweb/tornado/issues/2458
			if 300 <= response.code < 400:
				# NOTE: {KL} https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
				if response.code == 301 or response.code == 302:
					if not arguments['method'] in ['GET', 'HEAD']:
						# NOTE: The spec calls for user intervention here
						raise Error('User intervention is required')
				elif response.code == 303:
					arguments['method'] = 'GET'
					arguments.pop('body', None)
					arguments.pop('body_producer', None)
				elif response.code == 308:
					logging.warn('Use of deprecated endpoint')
				elif response.code in [305, 307]:
					pass
				else:
					raise NotImplementedError('Unsupported status code %d' % response.code)

				location = response.headers['location']
				arguments['follow_redirects'] = True

				url = urljoin(self.endpoint, location)

				# Strip the Authorization header on cross domain calls
				if urlparse(self.endpoint).netloc != urlparse(url).netloc:
					del headers['authorization']

				request = httpclient.HTTPRequest(url, **arguments)
				response = await self.client.fetch(request, raise_error=False)
			elif response.code == 403:
				if method == 'DELETE' and path == 'objects':
					raise ValueError('Forbidden')
			elif response.code == 502:
				# bad gateway
				if x == self.attempts - 1:
					raise ValueError('Connection reset (%d %s requests each %.1f seconds to /%s are failed).' % (self.attempts, method, self.sleep, path))
				# retry request
				logging.warning('Reconnecting...')
				time.sleep(self.sleep) # timeout to reduce load to API
				continue
			elif response.code >= 300:
				logging.error('%s /%s failed (%d %s)' % (method, path, response.code, response.reason))
			break

		if response.body:
			try:
				# for bodies in json format
				return json_decode(response.body)
			except:
				# for bodies in string format
				return response.body.decode('utf-8')

	def set_token(self, token):
		self.__token = token

	def get_token(self):
		return self.__token

	async def login(self):
		return await self.send_request(
			'login',
			method='POST',
			json={
				'email': self.__email,
				'password': self.__password
			}
		)

	async def status(self):
		return await self.send_request(
			'status',
			method='GET'
		)
