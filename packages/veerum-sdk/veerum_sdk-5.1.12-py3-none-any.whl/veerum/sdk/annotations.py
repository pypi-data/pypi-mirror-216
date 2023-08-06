import os
import sys
import logging
import mimetypes

from .base import BaseClient

class Client(BaseClient):
	async def find(self, workscope=None, organization=None, title=None, comment=None, resolved=None, sort=None, order=None, offset=None, limit=None, deleted=False):
		return await self.send_request(
			method='GET',
			path='annotations',
			query=self.pack(
				workscope=workscope,
				organization=organization,
				title=title,
				comment=comment,
				resolved=resolved,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit,
				deleted=deleted
			)
		)

	async def get(self, annotation):
		return await self.send_request(
			method='GET',
			path=self.join('annotations', annotation)
		)

	async def delete(self, annotation):
		return await self.send_request(
			method='DELETE',
			path=self.join('annotations', annotation)
		)
