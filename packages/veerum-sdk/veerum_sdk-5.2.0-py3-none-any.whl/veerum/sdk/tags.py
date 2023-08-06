from .base import BaseClient

class Client(BaseClient):
	async def create(self, workscope, name, values, colors):
		return await self.send_request(
			method='POST',
			path='tags',
			json=self.pack(
				workscope=workscope,
				name=name,
				values=values,
				colors=colors
			)
		)

	async def update(self, name, values, tag, colors):
		return await self.send_request(
			method='PUT',
			path=self.join('tags', tag),
			json=self.pack(
				name=name,
				values=values,
				colors=colors
			)
		)

	async def find(self, workscope=None):
		return await self.send_request(
			method='GET',
			path='tags',
			query=self.pack(**{
				'workscope[]': workscope,
			})
		)

	async def delete(self, workscope):
		return await self.send_request(
			method='DELETE',
			path='tags',
			query=self.pack(**{
				'workscope[]': workscope,
			})
		)

	async def deleteOne(self, tag):
		return await self.send_request(
			method='DELETE',
			path=self.join('tags', tag)
		)
