from .base import BaseClient
import logging


class Client(BaseClient):
    async def find(self, name=None, organization=None, parentId=None, tag=None, recursive=None, sort=None, order=None, offset=None, limit=None, units=None, xLabel=None, yLabel=None, labelMax=None, labelMin=None, labelLegend=None, heatmapMaxVal=None, heatmapUnits=None, path=None):
        return await self.send_request(
            method='GET',
            path='workscopes',
            query=self.pack(
                name=name,
                organization=organization,
                tag=tag,
                recursive=recursive,
                sort=sort,
                order=order,
                offset=offset,
                units=units,
                xLabel=xLabel,
                yLabel=yLabel,
                limit=limit,
                heatmapLabelMax=labelMax,
                heatmapLabelMin=labelMin,
                heatmapLabelLegend=labelLegend,
                heatmapMaxVal=heatmapMaxVal,
                heatmapUnits=heatmapUnits,
                parentId=parentId,
                path=path
            )
        )

    async def create(self, organization, name, position=None, parentId=None, description=None, units=None, xLabel=None, yLabel=None, labelMax=None, labelMin=None, labelLegend=None, heatmapMaxVal=None, heatmapUnits=None, path=None, defaultModels=None, showImages=None, pointSizeMode=None):
        return await self.send_request(
            method='POST',
            path='workscopes',
            json=self.pack(
                organization=organization,
                name=name,
                description=description,
                position=position,
                units=units,
                xLabel=xLabel,
                yLabel=yLabel,
                heatmapLabelMax=labelMax,
                heatmapLabelMin=labelMin,
                heatmapLabelLegend=labelLegend,
                heatmapMaxVal=heatmapMaxVal,
                heatmapUnits=heatmapUnits,
                parentId=parentId,
                path=path,
                defaultModels=defaultModels,
                showImages=showImages,
                pointSizeMode=pointSizeMode
            )
        )

    async def get(self, workscope):
        return await self.send_request(
            method='GET',
            path=self.join('workscopes', workscope)
        )

    async def update(self, workscope, organization=None, parentId=None, name=None, description=None, latitude=None, longitude=None, units=None, xLabel=None, yLabel=None, labelMax=None, labelMin=None, labelLegend=None, heatmapMaxVal=None, heatmapUnits=None, path=None, defaultModels=None, showImages=None, pointSizeMode=None):
        return await self.send_request(
            method='PATCH',
            path=self.join('workscopes', workscope),
            json=self.pack(
                name=name,
                description=description,
                latitude=latitude,
                longitude=longitude,
                units=units,
                xLabel=xLabel,
                yLabel=yLabel,
                heatmapLabelMax=labelMax,
                heatmapLabelMin=labelMin,
                heatmapLabelLegend=labelLegend,
                heatmapMaxVal=heatmapMaxVal,
                heatmapUnits=heatmapUnits,
                parentId=parentId,
                organization=organization,
                path=path,
                defaultModels=defaultModels,
                showImages=showImages,
                pointSizeMode=pointSizeMode
            )
        )

    async def all_tags(self, organization=None):
        return await self.send_request(
            method='GET',
            path=self.join('workscopes', 'tags'),
            query=self.pack(
                organization=organization
            )
        )

    async def get_tags(self, workscope):
        return await self.send_request(
            method='GET',
            path=self.join('workscopes', workscope, 'tags')
        )

    async def set_tags(self, workscope, *tags):
        return await self.send_request(
            method='PUT',
            path=self.join('workscopes', workscope, 'tags'),
            json=self.pack(
                tags=tags
            )
        )

    async def clear_tags(self, workscope):
        return await self.send_request(
            method='DELETE',
            path=self.join('workscopes', workscope, 'tags')
        )

    async def add_tag(self, workscope, tag):
        return await self.send_request(
            method='POST',
            path=self.join('workscopes', workscope, 'tags', tag),
            # NOTE: {KL} This is here because otherwise tornado requires that POST
            # has a body. Why allow_nonstandard_methods which in the documentation
            # should only effect the HTTP verb overrides that behaviour is beyond me.
            # See this disccusion on the IETF mailing list:
            # http://lists.w3.org/Archives/Public/ietf-http-wg/2010JulSep/0272.html
            allow_nonstandard_methods=True
        )

    async def remove_tag(self, workscope, tag):
        return await self.send_request(
            method='DELETE',
            path=self.join('workscopes', workscope, 'tags', tag)
        )

    async def add_feature(self, workscope, feature):
        return await self.send_request(
            method='POST',
            path=self.join('workscopes', workscope, 'features', feature),
            # NOTE: {KL} This is here because otherwise tornado requires that POST
            # has a body. Why allow_nonstandard_methods which in the documentation
            # should only effect the HTTP verb overrides that behaviour is beyond me.
            # See this disccusion on the IETF mailing list:
            # http://lists.w3.org/Archives/Public/ietf-http-wg/2010JulSep/0272.html
            allow_nonstandard_methods=True
        )

    async def remove_feature(self, workscope, feature):
        return await self.send_request(
            method='DELETE',
            path=self.join('workscopes', workscope, 'features', feature)
        )

    async def delete(self, workscope, hash=None):
        return await self.send_request(
            method='DELETE',
            path=self.join('workscopes', workscope),
            query=self.pack(
                hash=hash
            )
        );