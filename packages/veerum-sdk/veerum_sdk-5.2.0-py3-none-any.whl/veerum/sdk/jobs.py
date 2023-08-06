from .base import BaseClient

class Client(BaseClient):
	async def warn_inactive_users(self):
		return await self.send_request(
			method='POST',
			path=self.join('cronjobs', 'inactive_users'),
			json={}
		)
	async def populate_keys(self):
		return await self.send_request(
			method='PATCH',
			path=self.join('cronjobs', 'populate_keys'),
			json={}
		)
	async def misplaced_objects(self):
		return await self.send_request(
			method='PATCH',
			path=self.join('cronjobs', 'misplaced_objects'),
			json={}
		)

