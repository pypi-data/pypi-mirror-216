import os

from .base import BaseClient


class Client(BaseClient):

	async def sync(self, workscope, search_field, model=None):
		return await self.send_request(
			method='POST',
			path='automations/sync',
			json=self.pack(
				workscopeId=workscope,
				search_field=search_field,
				model_id=model
			)
		)
	async def relationship(self, workscope, model=None):
		return await self.send_request(
			method='POST',
			path='automations/relationship',
			json=self.pack(
				workscopeId=workscope,
				model_id=model
			)
		)