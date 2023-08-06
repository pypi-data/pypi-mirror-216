import os

from .base import BaseClient


class Client(BaseClient):
	async def find(
		self,
		workscope=None,
		organization=None,
		format=None,
		type=None,
		start=None,
		end=None,
		sort=None,
		order=None,
		offset=None,
		limit=None,
		category=None
	):
		return await self.send_request(
			method='GET',
			path='models',
			query=self.pack(
				workscope=workscope,
				organization=organization,
				format=format,
				type=type,
				startDate=start,
				endDate=end,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit,
				category=category
			)
		)

	async def create(self, workscope, date, format, type, name, description=None, category=None, auto2d=False):
		return await self.send_request(
			method='POST',
			path='models',
			json=self.pack(
				workscope=workscope,
				date=date,
				format=format,
				type=type,
				name=name,
				description=description,
				category=category,
				auto2d=auto2d
			)
		)

	async def get(self, model):
		return await self.send_request(
			method='GET',
			path=self.join('models', model)
		)

	async def update(
		self,
		model,
		workscope=None,
		date=None,
		name=None,
		description=None,
		type=None,
		category=None,
		auto2d=False
	):
		return await self.send_request(
			method='PATCH',
			path=self.join('models', model),
			json=self.pack(
				workscope=workscope,
				date=date,
				name=name,
				description=description,
				type=type,
				category=category,
				auto2d=auto2d
			)
		)

	async def delete(self, model):
		return await self.send_request(
			method='DELETE',
			path=self.join('models', model)
		)

	async def upload_file(self, model, key, filename, mimetype, encoding):
		with open(filename, 'rb') as stream:
			return await self.upload_stream(
				model, key, stream, mimetype,
				encoding,
				size=os.path.getsize(filename),
			)

	async def upload_stream(self, model, key, stream, mimetype, encoding, size=None):
		if not size is None:
			size = str(size)

		return await self.send_request(
			method='PUT',
			path=self.join('models', model, key),
			headers=self.pack(**{
				'content-type': mimetype,
				'content-length': size,
				'content-encoding': encoding,
			}),
			body=stream,
			request_timeout=float('+inf')
		)

	async def abort_multipart(self, model_id):
		return await self.send_request(
			method='GET',
			path=self.join('models/abort-multipart', model_id)
		)

	async def set_metadata(self, model, data):
		return await self.send_request(
			method='PUT',
			path=self.join('models/metadata', model),
			json=data
		)

	async def delete_metadata(self, model):
		return await self.send_request(
			method='DELETE',
			path=self.join('models/metadata', model)
		)
