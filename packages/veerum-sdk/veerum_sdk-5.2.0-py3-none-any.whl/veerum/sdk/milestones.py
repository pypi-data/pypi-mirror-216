from .base import BaseClient

class Client(BaseClient):
	async def find(self, workscope=None, organization=None, start=None, end=None, offset=None, limit=None):
		return await self.send_request(
			method='GET',
			path='milestones',
			query=self.pack(
				workscope=workscope,
				organization=organization,
				startDate=start,
				endDate=end,
				offset=offset,
				limit=limit
			)
		)

	async def create(self, workscope, date, label, critical=False, source=None, target=None, line_color=None, line_width=None):
		return await self.send_request(
			method='POST',
			path='milestones',
			json=self.pack(
				workscope=workscope,
				date=date,
				label=label,
				critical=critical,
				source=source,
				target=target,
				lineColor=line_color,
				lineWidth=line_width,
			)
		)

	async def update(self, milestone, workscope=None, date=None, label=None, critical=None, source=None, target=None, line_color=None, line_width=None):
		return await self.send_request(
			method='PATCH',
			path=self.join('milestones', milestone),
			json=self.pack(
				workscope=workscope,
				date=date,
				label=label,
				critical=critical,
				source=source,
				target=target,
				lineColor=line_color,
				lineWidth=line_width,
			)
		)

	async def delete(self, milestone):
		return await self.send_request(
			method='DELETE',
			path=self.join('milestones', milestone)
		)

	async def get(self, milestone):
		return await self.send_request(
			method='GET',
			path=self.join('milestones', milestone)
		)
