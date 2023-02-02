"""Copyright (C) 2023 Kevin Morris"""
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


def api_request(request_uri: str, user: str):
    session = requests_unixsocket.Session()
    uri = quote_plus(settings.WEBVIRTD_SOCKET)
    status_code = HTTPStatus.OK
    data = {}
    try:
        response = session.post(
            f"http+unix://{uri}{request_uri}",
            data=json.dumps({"user": user}),
        )

        status_code = response.status_code
        data = response.json()
    except ConnectionError:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        data["detail"] = "Unable to connect to webvirtd"

    return (status_code, data)


@api_view(["GET", "POST"])
@permissions([IsAuthenticated])
def http_request(request: Request, *args, **kwargs) -> Response:
    user = request.user.username
    status_code, data = api_request(request.path, user)
    return Response(data, status_code)
