from .base import BaseClient


class Client(BaseClient):
    def update(self,
               organization,
               rateLimitUsers=None,
               rateLimitAnnotations=None,
               rateLimitFiles=None,
               rateLimitModels=None,
               rateLimitWorkscopes=None,
               rateLimitObjectsSearch=None,
               rateLimitObjectsSpatialSearch=None
               ):
        return self.send_request(
            method='PATCH',
            path=self.join('organization-configs', organization),
            json=self.pack(
                rateLimit_users=rateLimitUsers,
                rateLimit_annotations=rateLimitAnnotations,
                rateLimit_files=rateLimitFiles,
                rateLimit_models=rateLimitModels,
                rateLimit_workscopes=rateLimitWorkscopes,
                rateLimit_objects_search=rateLimitObjectsSearch,
                rateLimit_objects_spatial_search=rateLimitObjectsSpatialSearch
            )
        )

    def get(self, organization):
        return self.send_request(
            method='GET',
            path=self.join('organization-configs', organization)
        )
