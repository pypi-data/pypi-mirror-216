"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import itertools
import json
import logging
import requests

from typing import Generator

from ..config import Config
from .datatypes import (
    StellaEntity,
    StellaField,
    StellaEvent,
    StellaEventDetailed
)
from ..exceptions.api_exceptions import (
    StellaAPIForbiddenError,
    StellaAPINotFoundError,
    StellaAPIUnauthorisedError,
    StellaAPIWrongCredentialsError
)


logger = logging.getLogger(__name__)


class StellaAPI:
    def __init__(self, env_config: Config, access_key: str, access_token: str, organization_id: str, project_id: str):
        self.env_config = env_config

        self.access_key = access_key
        self.access_token = access_token
        self.organization_id = organization_id
        self.project_id = project_id
        self.auth_token = None
        self.refresh_token = None

        self.authenticate()

    def _handle_response(self, response):
        try:
            details = response.json().get("details", dict())
        except json.JSONDecodeError:
            details = dict()

        match response.status_code:
            case 401:
                errors = details.get("errors", list())

                for error in errors:
                    match error.get("errorCode"):
                        case "inactiveAuthToken":
                            self.auth_refresh()
                            return
                        case "wrongUsernameOrPassword":
                            raise StellaAPIWrongCredentialsError()
                        case _:
                            raise StellaAPIUnauthorisedError(details)
                else:
                    response.raise_for_status()
            case 403:
                raise StellaAPIForbiddenError()
            case 404:
                raise StellaAPINotFoundError(details)
            case _:
                response.raise_for_status()

    def authenticate(self):
        logger.info("Authenticating to the API ... ")

        if self.refresh_token is not None:
            self.auth_refresh()
        else:
            body = {
                "realm_id": self.organization_id,
                "username": self.access_key,
                "email": self.access_key,
                "password": self.access_token,
                "client_id": "backoffice"
            }

            self.auth_token = None
            self.refresh_token = None

            response = requests.post(self.env_config.auth_url, json=body)
            self._handle_response(response)

            self.auth_token = response.json().get("details", dict()).get("access_token")
            self.refresh_token = response.json().get("details", dict()).get("refresh_token")

        logger.info("Authentication Successful")

    def auth_refresh(self):
        if self.refresh_token is None:
            self.authenticate()
        else:
            logger.info("API Token Refreshing ...")

            body = {"refresh_token": self.refresh_token}

            self.auth_token = None
            self.refresh_token = None

            response = requests.post(self.env_config.auth_refresh_url, json=body)
            self._handle_response(response)

            self.auth_token = response.json().get("details", dict()).get("access_token")
            self.refresh_token = response.json().get("details", dict()).get("refresh_token")

            logger.info("API Token Refresh Successful")

    def get_events(self) -> Generator[StellaEvent, None, None]:
        page_size = 100
        for page_number in itertools.count(1, 1):
            url = self.env_config.events_url.format(projectId=self.project_id) + \
                  f"?page={page_number}&pageSize={page_size}&filter=IncludeInactive"
            headers = {"Authorization": f"Bearer {self.auth_token}"}

            response = requests.get(url, headers=headers)
            self._handle_response(response)

            events = response.json().get("details", dict()).get("results", [])
            if not events:
                break

            yield from (
                StellaEvent(
                    id=event.get('id'),
                    name=event.get('name'),
                    isActive=event.get('isActive'),
                    createdAt=event.get('createdAt'),
                    updatedAt=event.get('updatedAt')
                ) for event in events
            )

    def get_event_details(self, event_id: str) -> StellaEventDetailed:
        url = self.env_config.event_url.format(projectId=self.project_id, eventId=event_id)
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = requests.get(url, headers=headers)
        self._handle_response(response)

        details = response.json().get("details", dict())

        # create StellaEntity objects from the 'entities' list
        entities = [StellaEntity(**entity) for entity in details.get('entities', list())]

        # create StellaField objects from the 'fields' list
        fields = [StellaField(**field) for field in details.get('fields', list())]

        # create and return StellaEventDetailed object
        return StellaEventDetailed(
            id=details.get('id'),
            name=details.get('name'),
            description=details.get('description'),
            isActive=details.get('isActive'),
            createdAt=details.get('createdAt'),
            updatedAt=details.get('updatedAt'),
            fields=fields,
            entities=entities,
        )
