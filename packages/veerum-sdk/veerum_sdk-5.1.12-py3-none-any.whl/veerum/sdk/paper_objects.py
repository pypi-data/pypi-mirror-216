import os

from .base import BaseClient


class Client(BaseClient):

	def find(self, file, object=None, sort=None, order=None, skip=None, limit=None):
		return self.send_request(
			method='GET',
			path='paper-objects',
			query=self.pack(
				file_id=file,
				object_id=object,
				sort= sort,
				order= order,
				skip= skip,
				limit= limit
			)
		)

	async def create(self, workscope, organization, object, file, text, bbox, page, color=None):
		return await self.send_request(
			method='POST',
			path='paper-objects',
			json=self.pack(
				workscopeId=workscope,
				organizationId=organization,
				object_id=object,
				file_id=file,
				text=text,
				bbox=bbox,
				color=color,
				page=page
			)
		)

	async def get(self, paperObject):
		return await self.send_request(
			method='GET',
			path=self.join('paper-objects', paperObject)
		)

	async def delete(self, paperObject):
		return await self.send_request(
			method='DELETE',
			path=self.join('paper-objects', paperObject)
		)

	async def delete_many(self, file=None, object=None):
		return await self.send_request(
			method='DELETE',
			path='paper-objects',
			query=self.pack(
				file_id=file,
				object_id=object
			)
		)

	async def bulk_create(self, paperObjects):
		return await self.send_request(
			method='POST',
			path='paper-objects',
			json=self.pack(
				bulk=paperObjects
			)
		)

	async def update(self, paperObject, text = None, bbox = None, page = None, color = None, object = None):
		return await self.send_request(
			method='PATCH',
			path=self.join('paper-objects', paperObject),
			json=self.pack(
				object_id=object,
				text=text,
				bbox=bbox,
				color=color,
				page=page
			)
		)
