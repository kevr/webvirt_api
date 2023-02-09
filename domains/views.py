# Copyright 2023 Kevin Morris
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
import json
from http import HTTPStatus
from urllib.parse import quote_plus

import requests_unixsocket
from django.conf import settings
from requests.exceptions import ConnectionError
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes as permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


def api_request(
    request_fn, request_uri: str, user: str, data: dict[str, str] = {}
):
    uri = quote_plus(settings.WEBVIRTD_SOCKET)
    user = quote_plus(user)
    status_code = HTTPStatus.OK
    try:
        response = request_fn(
            f"http+unix://{uri}/users/{user}{request_uri}",
            data=data,
        )

        status_code = response.status_code
        try:
            data = response.json()
        except Exception:
            data = {}

    except ConnectionError:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        data["detail"] = "Unable to connect to webvirtd"

    return (status_code, data)


@api_view(["GET", "POST", "DELETE"])
@permissions([IsAuthenticated])
def http_request(request: Request, *args, **kwargs) -> Response:
    session = requests_unixsocket.Session()
    request_fn = getattr(session, request.method.lower())

    data = {}
    try:
        data = json.loads(request.body.decode())
    except Exception:
        pass

    status_code, data = api_request(
        request_fn,
        request.path,
        request.user.username,
        data=data,
    )
    return Response(data, status_code)
