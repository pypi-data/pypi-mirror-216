import os

from .base import BaseClient


class Client(BaseClient):

	async def create(self, workscope, model, metadata):
		return await self.send_request(
			method='POST',
			path='objects',
			json=self.pack(
				workscope=workscope,
				model=model,
				metadata=metadata,
				allow_html=True
			)
		)

	async def get(self, object):
		return await self.send_request(
			method='GET',
			path=self.join('objects', object)
		)

	async def deleteOne(self, object):
		return await self.send_request(
			method='DELETE',
			path=self.join('objects', object)
		)

	async def delete(self, workscope, model):
		def streaming_callback(chunk):
			print(chunk.decode('utf-8')) # printing progress

		return await self.send_request(
			method='DELETE',
			path='objects',
			allow_nonstandard_methods=True,
			query=self.pack(
				workscope=workscope,
				model=model
			),
			streaming_callback=streaming_callback
		)

	async def bulk_create(self, workscope, model, objects):
		return await self.send_request(
			method='POST',
			path='objects',
			json=self.pack(
				workscope=workscope,
				model=model,
				bulk=objects,
				allow_html=True
			)
		)

	async def find(self, workscope=None, model=None, sort=None, order=None, skip=None, limit=None):
		return await self.send_request(
			method='GET',
			path=self.join('objects', 'search'),
			query=self.pack(**{
				'workscopes[]': workscope,
				'models[]': model,
				'sort': sort,
				'order': order,
				'skip': skip,
				'limit': limit
			})
		)

	async def update(self, object, workscope, model, position, scale, orientation, metadata):
		return await self.send_request(
			method='PATCH',
			path=self.join('objects', object),
			json=self.pack(
				workscope=workscope,
				model=model,
				position=position,
				scale=scale,
				orientation=orientation,
				metadata=metadata,
				allow_html=True
			)
		)

	async def upload_file(self, organization, key, filename, rel_path, mimetype):
		with open(filename, 'rb') as stream:
			return await self.upload_stream(
				organization, stream, rel_path, mimetype,
				size=os.path.getsize(filename)
			)

	async def upload_stream(self, organization, stream, rel_path, mimetype, size=None):
		if not size is None:
			size = str(size)

		return await self.send_request(
			method='PUT',
			path=self.join('objects/pano', organization, rel_path),
			headers=self.pack(**{
				'content-type': mimetype,
				'content-length': size,
			}),
			body=stream,
			request_timeout=float('+inf')
		)
