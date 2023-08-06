import os

from .base import BaseClient

class Client(BaseClient):
	async def find(self, workscope=None, organization=None, name=None, mimetype=None, uploaded=None, sort=None, order=None, offset=None, limit=None, start=None, end=None):
		return await self.send_request(
			method='GET',
			path='files',
			query=self.pack(
				workscope=workscope,
				organization=organization,
				name=name,
				mimetype=mimetype,
				uploaded=uploaded,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit,
				startDate = start,
				endDate = end
			)
		)

	async def create(self, workscope, date, name, description=None):
		return await self.send_request(
			method='POST',
			path='files',
			json=self.pack(
				workscope=workscope,
				name=name,
				date=date,
				description=description
			)
		)

	async def get(self, file):
		return await self.send_request(
			method='GET',
			path=self.join('files', file)
		)

	async def update(self, file, workscope=None, date=None, name=None, description=None):
		return await self.send_request(
			method='PATCH',
			path=self.join('files', file),
			json=self.pack(
				workscope=workscope,
				date=date,
				name=name,
				description=description
			)
		)

	async def delete(self, file):
		return await self.send_request(
			method='DELETE',
			path=self.join('files', file)
		)

	async def upload_file(self, file, filename, mimetype):
		with open(filename, 'rb') as stream:
			return await self.upload_stream(
				file, stream,
				mimetype=mimetype,
				size=os.path.getsize(filename)
			)

	async def upload_stream(self, file, stream, mimetype, size=None):
		if not size is None:
			size = str(size)

		return await self.send_request(
			method='PUT',
			path=self.join('files', file, 'upload'),
			headers=self.pack(**{
				'content-type': mimetype,
				'content-length': size,
			}),
			body=stream,
			request_timeout=float('+inf')
		)

	async def download_file(self, file, filename):
		with open(filename, 'wb') as stream:
			return await self.download_stream(file, stream)

	async def download_stream(self, file, stream):
		def write_to_stream(chunk):
			stream.write(chunk)

		return await self.send_request(
			method='GET',
			path=self.join('files', file, 'download'),
			streaming_callback=write_to_stream
		)
