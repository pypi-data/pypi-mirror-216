from .base import BaseClient

class Client(BaseClient):
	async def find(self, email=None, name=None, phone=None, pwned=None, sort=None, order=None, offset=None, limit=None):
		return await self.send_request(
			method='GET',
			path='users',
			query=self.pack(
				email=email,
				name=name,
				phone=phone,
				pwned=pwned,
				sort=sort,
				order=order,
				offset=offset,
				limit=limit
			)
		)

	async def create(self, email, name=None, phone=None, workscopes=None, organizations=None, wsViewRights=None):
		return await self.send_request(
			method='POST',
			path='users',
			json=self.pack(
				email=email,
				name=name,
				phone=phone,
				workscopes=workscopes,
				organizations=organizations,
				wsViewRights=wsViewRights
			)
		)

	async def get(self, user):
		return await self.send_request(
			method='GET',
			path=self.join('users', user)
		)

	async def update(self, user, email=None, name=None, phone=None, disabled=None, sso=None, wsViewRights=None):
		return await self.send_request(
			method='PATCH',
			path=self.join('users', user),
			json=self.pack(
				email=email,
				name=name,
				phone=phone,
				disabled=disabled,
				sso=sso,
				wsViewRights=wsViewRights
			)
		)

	async def find_organizations(self, user):
		return await self.send_request(
			method='GET',
			path=self.join('users', user, 'organizations')
		)

	async def join_organization(self, user, organization):
		return await self.send_request(
			method='POST',
			path=self.join('users', user, 'organizations', organization),
			# NOTE: {KL} This is here because otherwise tornado requires that POST
			# has a body. Why allow_nonstandard_methods which in the documentation
			# should only effect the HTTP verb overrides that behaviour is beyond me.
			# See this disccusion on the IETF mailing list:
			# http://lists.w3.org/Archives/Public/ietf-http-wg/2010JulSep/0272.html
			allow_nonstandard_methods=True
		)

	async def leave_organization(self, user, organization):
		return await self.send_request(
			method='DELETE',
			path=self.join('users', user, 'organizations', organization)
		)

	async def find_workscopes(self, user):
		return await self.send_request(
			method='GET',
			path=self.join('users', user, 'workscopes')
		)

	async def join_workscope(self, user, workscope):
		return await self.send_request(
			method='POST',
			path=self.join('users', user, 'workscopes', workscope),
			# NOTE: {KL} This is here because otherwise tornado requires that POST
			# has a body. Why allow_nonstandard_methods which in the documentation
			# should only effect the HTTP verb overrides that behaviour is beyond me.
			# See this disccusion on the IETF mailing list:
			# http://lists.w3.org/Archives/Public/ietf-http-wg/2010JulSep/0272.html
			allow_nonstandard_methods=True
		)

	async def leave_workscope(self, user, workscope):
		return await self.send_request(
			method='DELETE',
			path=self.join('users', user, 'workscopes', workscope)
		)
