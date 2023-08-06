import os

from veerum.utils.helpers import File
from .base import BaseClient


class Client(BaseClient):
	async def find(self, model=None, organization=None, start=None, end=None, sort=None, order=None, offset=None, limit=None):
		return await self.send_request(
			method='GET',
			path='metadata',
			query=self.pack(
				model=model,
				organization=organization,
				startDate=start,
				endDate=end,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit
			)
		)
	
	async def create_metadata(self, object, metadata):
		return await self.send_request(
			method='POST',
			path='metadata_new',
			json=self.pack(
				object=object,
				metadata=metadata
			)
		)

	async def create_object(self, model, metadata):
		return await self.send_request(
			method='POST',
			path='objects',
			json=self.pack(
				model=model,
				metadata=metadata
			)
		)

	async def create(self, model, date, description=None):
		return await self.send_request(
			method='POST',
			path='metadata',
			json=self.pack(
				model=model,
				date=date,
				description=description
			)
		)

	async def finalize(self, metadata, model):
		return await self.send_request(
			method='PATCH',
			path=self.join('metadata', metadata, 'finalize'),
			json=self.pack(
				model=model
			)
		)

	async def get(self, model):
		return await self.send_request(
			method='GET',
			path=self.join('metadata', model)
		)

	async def upload_files(self, metadata, file):
		path = os.path.splitext(file.path)[0] + '.csv'
		filename = os.path.splitext(file.key)[0] + '.csv'
		pair = File(filename, path, 'text/csv')

		return await self.send_request(
			method='PUT',
			path=self.join('metadata', metadata, file.key),
			headers=self.pack(**{
				'content-type': 'multipart/form-data',
			}),
			request_timeout=float('+inf'),
			files=[file, pair]
		)

	async def upload_file(self, metadata, file):
		with open(file.path, 'rb') as stream:
			return await self.upload_stream(
				metadata,
				file.key,
				stream,
				file.mimetype,
				size=file.size
			)

	async def upload_stream(self, metadata, key, stream, mimetype, size=None):
		if not size is None:
			size = str(size)

		return await self.send_request(
			method='PUT',
			path=self.join('metadata', metadata, key),
			headers=self.pack(**{
				'content-type': mimetype,
				'content-length': size,
			}),
			body=stream,
			request_timeout=float('+inf')
		)

	async def all_keys(self, organization=None):
		return await self.send_request(
			method='GET',
			path=self.join('metadata', 'keys'),
			query=self.pack(
				organization=organization
			)
		)

	async def get_keys(self, model):
		return await self.send_request(
			method='GET',
			path=self.join('metadata', 'keys', model)
		)

	async def set_keys(self, model, *keys):
		return await self.send_request(
			method='PUT',
			path=self.join('metadata', 'keys', model),
			json=self.pack(
				keys=keys
			)
		)

	async def clear_keys(self, model):
		return await self.send_request(
			method='DELETE',
			path=self.join('metadata', 'keys', model)
		)

	async def add_key(self, model, key):
		return await self.send_request(
			method='POST',
			path=self.join('metadata', 'keys', model, key),
			# NOTE: {KL} This is here because otherwise tornado requires that POST
			# has a body. Why allow_nonstandard_methods which in the documentation
			# should only effect the HTTP verb overrides that behaviour is beyond me.
			# See this disccusion on the IETF mailing list:
			# http://lists.w3.org/Archives/Public/ietf-http-wg/2010JulSep/0272.html
			allow_nonstandard_methods=True
		)
