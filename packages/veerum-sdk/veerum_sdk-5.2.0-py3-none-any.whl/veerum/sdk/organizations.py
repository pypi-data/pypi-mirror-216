import json
from .base import BaseClient


class Client(BaseClient):
    def find(self, name=None, sort=None, order=None, offset=None, limit=None):
        return self.send_request(
            method='GET',
            path='organizations',
            query=self.pack(
                name=name,
                sort=sort,
                order=order,
                offset=offset,
                limit=limit
            )
        )

    def create(self,
               name,
               slug,
               ninenine=False,
               nonUseLockPeriodDays=None,
               pwdExpiresInDays=None,
               maxLockoutAttempts=None,
               timeOfInactivityInSecs=None,
               auth0ConnId=None,
               auth0ClientId=None,
               hundred=False
               ):
        return self.send_request(
            method='POST',
            path='organizations',
            json=self.pack(
                name=name,
                slug=slug,
                ninenine=ninenine,
                nonUseLockPeriodDays=nonUseLockPeriodDays,
                pwdExpiresInDays=pwdExpiresInDays,
                maxLockoutAttempts=maxLockoutAttempts,
                timeOfInactivityInSecs=timeOfInactivityInSecs,
                auth0ConnId=auth0ConnId,
                auth0ClientId=auth0ClientId,
                hundred=hundred
            )
        )

    def get(self, organization):
        return self.send_request(
            method='GET',
            path=self.join('organizations', organization)
        )

    def update(self,
               organization,
               name=None,
               nonUseLockPeriodDays=None,
               pwdExpiresInDays=None,
               maxLockoutAttempts=None,
               timeOfInactivityInSecs=None,
               auth0ConnId=None,
               auth0ClientId=None,
               defaultOrgWs=None
               ):
        return self.send_request(
            method='PATCH',
            path=self.join('organizations', organization),
            json=self.pack(
                name=name,
                nonUseLockPeriodDays=nonUseLockPeriodDays,
                pwdExpiresInDays=pwdExpiresInDays,
                maxLockoutAttempts=maxLockoutAttempts,
                timeOfInactivityInSecs=timeOfInactivityInSecs,
                auth0ConnId=auth0ConnId,
                auth0ClientId=auth0ClientId,
                defaultOrgWs=defaultOrgWs
            )
        )

    def delete(self, organization):
        return self.send_request(
            method='DELETE',
            path=self.join('organizations', organization)
        )

    def get_integrations(self, organization):
        return self.send_request(
            method='GET',
            path=self.join('organizations', organization, 'integrations')
        )

    def update_integration(self, organization, integration, packed):
        return self.send_request(
            method='PATCH',
            path=self.join('organizations', organization, 'integrations', integration),
            json=packed
        )

    def create_integration(self, organization, packed):
        return self.send_request(
            method='POST',
            path=self.join('organizations', organization, 'integrations'),
            json=packed
        )

    def delete_integration(self, organization, integration):
        return self.send_request(
            method='DELETE',
            path=self.join('organizations', organization, 'integrations', integration)
        )

    def integration_handler(self, organization, integration, payload):
        packed = self.pack(**payload)

        if integration is not None:
            return self.update_integration(organization, integration, packed)

        return self.create_integration(organization, packed)

    def wms_integration(self, organization, endpoint, layers, integration=None):
        payload = integration_payload('WMS', endpoint, {'layers': [*layers]})
        return self.integration_handler(organization, integration, payload)

    def pi_system_integration(self,
                              organization, cron, endpoint, other_data_tuple,
                              integration=None):
        username, userpassword, assetservername, assetdatabasename = other_data_tuple
        other_data = {
            'username': username,
            'userpassword': userpassword,
            'assetservername': assetservername,
            'assetdatabasename': assetdatabasename
        }
        payload = integration_payload('pi_system', endpoint, other_data, cron)
        return self.integration_handler(organization, integration, payload)

    def maximo_integration(self, organization, cron,
                           endpoint, apikey,
                           integration=None):
        payload = integration_payload('maximo', endpoint, {'apikey': apikey}, cron)
        return self.integration_handler(organization, integration, payload)

    def watson_ir_integration(self, organization, cron, integration=None):
        payload = integration_payload('watson_ir', cron=cron)
        return self.integration_handler(organization, integration, payload)

    def iol_sap_integration(self, organization, cron, integration=None):
        payload = integration_payload('iol_sap', cron=cron)
        return self.integration_handler(organization, integration, payload)


def integration_payload(integration_type, endpoint=None, other_data={}, cron=None):
    return {
        'type': integration_type,
        'cron': cron,
        'data': {
            'endpoint': endpoint,
            **other_data
        }
    }
