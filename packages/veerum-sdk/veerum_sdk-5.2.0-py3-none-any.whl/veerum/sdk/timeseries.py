from .base import BaseClient

class Client(BaseClient):
	async def find(self, workscope=None, organization=None, name=None, type=None, current=None, start=None, end=None, sort=None, order=None, offset=None, limit=None):
		return await self.send_request(
			method='GET',
			path='timeseries',
			query=self.pack(
				workscope=workscope,
				organization=organization,
				name=name,
				type=type,
				current=current,
				startDate=start,
				endDate=end,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit
			)
		)

	async def create(self, workscope, x_unit=None, y_unit=None, x_label=None, y_label=None, current=None, name=None, type=None, point_style=None, point_color=None, chart_radius=None):
		return await self.send_request(
			method='POST',
			path='timeseries',
			json=self.pack(
				workscope=workscope,
				xUnit=x_unit,
				yUnit=y_unit,
				xLabel=x_label,
				yLabel=y_label,
				current=current,
				name=name,
				type=type,
				chartPointStyle=point_style,
				chartBorderColor=point_color,
				chartRadius=chart_radius,
			)
		)

	async def get(self, timeseries):
		return await self.send_request(
			method='GET',
			path=self.join('timeseries', timeseries)
		)

	async def update(self, timeseries, workscope=None, x_unit=None, y_unit=None, x_label=None, y_label=None, current=None, name=None, type=None, point_style=None, point_color=None, chart_radius=None):
		return await self.send_request(
			method='PATCH',
			path=self.join('timeseries', timeseries),
			json=self.pack(
				workscope=workscope,
				xUnit=x_unit,
				yUnit=y_unit,
				xLabel=x_label,
				yLabel=y_label,
				current=current,
				name=name,
				type=type,
				chartPointStyle=point_style,
				chartBorderColor=point_color,
				chartRadius=chart_radius,
			)
		)

	async def delete(self, timeseries):
		return await self.send_request(
			method='DELETE',
			path=self.join('timeseries', timeseries)
		)

	async def get_data(self, timeseries):
		return await self.send_request(
			method='GET',
			path=self.join('timeseries', timeseries, 'data')
		)

	async def add_data(self, timeseries, x, y):
		return await self.send_request(
			method='POST',
			path=self.join('timeseries', timeseries, 'data'),
			json=self.pack(
				x=x, y=y
			)
		)

	async def remove_data(self, timeseries, data):
		return await self.send_request(
			method='DELETE',
			path=self.join('timeseries', timeseries, 'data', data)
		)

	async def set_data(self, timeseries, *data):
		return await self.send_request(
			method='PUT',
			path=self.join('timeseries', timeseries, 'data'),
			json=self.pack(
				data=data
			)
		)

	async def clear_data(self, timeseries):
		return await self.send_request(
			method='DELETE',
			path=self.join('timeseries', timeseries, 'data')
		)
