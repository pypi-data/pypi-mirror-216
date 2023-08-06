# Copyright 2023 Anton Karmanov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is a part of Pixelfeeder utility. Pixelfeeder helps to migrate data
# from Flickr to a Pixelfed instance.

import asyncio
import json
import logging
import mimetypes
import ssl

from pprint import pformat
from typing import Dict, List, Optional

import httpx

from pixelfeeder.tools import PathUnion, PixelfedVisibility


class PixelfedClientError(RuntimeError):
    ...


class PixelfedClientConnectionError(PixelfedClientError):
    ...


class PixelfedClientRequestError(PixelfedClientError):
    ...


class PixelfedClient:
    MEDIA_ENDPOINT = '/api/v1/media'
    STATUSES_ENDPOINT = '/api/v1/statuses'

    def __init__(self, base_url: str, token: str, strict_ssl=True) -> None:
        self.base_url = base_url
        self._headers = {
            'Authorization': f"Bearer {token}",
            'Accept': 'application/json',
        }
        self._client_kwargs = {'verify': strict_ssl}
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def _post_media(self, file_path: PathUnion) -> str:
        with open(file_path, 'rb') as file:
            media = file.read()

        mimetype, _enc = mimetypes.guess_type(file_path)

        files_payload = {
            'file': (file_path, media, mimetype),
        }
        url = self.base_url + self.MEDIA_ENDPOINT
        resp = await self._post(url, files=files_payload)
        media_id = resp.json()['id']
        return media_id

    async def _post_status(self, media_ids: List[str], caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        data = {
            'status': caption,
            'media_ids[]': media_ids,
            'sensitive:': False,  # Seems ignored
            'visibility': visibility.value,
        }
        url = self.base_url + self.STATUSES_ENDPOINT
        resp = await self._post(url, data=data)
        return resp.json()['url']

    async def create_post(self, file_path: PathUnion, caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        media_id = await self._post_media(file_path)
        result = await self._post_status([media_id], caption, visibility)
        return result

    def blocking_create_post(self, file_path: PathUnion, caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        coro = self.create_post(file_path, caption, visibility)
        return asyncio.run(coro)

    async def _post(self, url: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> httpx.Response:
        try:
            async with httpx.AsyncClient(**self._client_kwargs) as client:
                resp = await client.post(
                    url=url,
                    headers=self._headers,
                    data=data,
                    files=files)
        except (httpx.HTTPError, ssl.SSLCertVerificationError) as error:
            raise PixelfedClientConnectionError(error) from error

        content_type = resp.headers.get('content-type', '')

        if content_type.lower() == 'application/json':
            data = resp.json()
            self.logger.debug('Response headers:\n' + pformat(dict(resp.headers, indent=2)))
            self.logger.debug('Response content:\n' + json.dumps(data, indent=2))
        else:
            self.logger.debug('Response headers:\n' + json.dumps(resp.headers, indent=2))
            self.logger.warning(f'Response with unexpected Content-Type "{content_type}"')

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise PixelfedClientRequestError(error) from error

        return resp
