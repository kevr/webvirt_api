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
from rest_framework.views import APIView


class DomainsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user.username
        session = requests_unixsocket.Session()
        uri = quote_plus(settings.WEBVIRTD_SOCKET)

        status_code = HTTPStatus.OK
        data = {}
        try:
            response = session.post(
                f"http+unix://{uri}/domains/",
                data=json.dumps({"user": user}),
            )

            status_code = response.status_code
            data = response.json()
        except ConnectionError:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            data["detail"] = "Unable to connect to webvirtd"

        return Response(data, status=status_code)


class DomainView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, name: str) -> Response:
        user = request.user.username
        session = requests_unixsocket.Session()
        uri = quote_plus(settings.WEBVIRTD_SOCKET)

        status_code = HTTPStatus.OK
        data = {}
        try:
            response = session.post(
                f"http+unix://{uri}/domains/{name}/",
                data=json.dumps({"user": user}),
            )

            status_code = response.status_code
            data = response.json()
        except ConnectionError:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            data["detail"] = "Unable to connect to webvirtd"

        return Response(data, status_code)


@api_view(["POST"])
@permissions([IsAuthenticated])
def domain_start(request: Request, name: str) -> Response:
    user = request.user.username
    session = requests_unixsocket.Session()
    uri = quote_plus(settings.WEBVIRTD_SOCKET)

    status_code = HTTPStatus.OK
    data = {}
    try:
        response = session.post(
            f"http+unix://{uri}/domains/{name}/start/",
            data=json.dumps({"user": user}),
        )

        status_code = response.status_code
        data = response.json()
    except ConnectionError:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        data["detail"] = "Unable to connect to webvirtd"

    return Response(data, status_code)


@api_view(["POST"])
@permissions([IsAuthenticated])
def domain_shutdown(request: Request, name: str) -> Response:
    user = request.user.username
    session = requests_unixsocket.Session()
    uri = quote_plus(settings.WEBVIRTD_SOCKET)

    status_code = HTTPStatus.OK
    data = {}
    try:
        response = session.post(
            f"http+unix://{uri}/domains/{name}/shutdown/",
            data=json.dumps({"user": user}),
        )

        status_code = response.status_code
        data = response.json()
    except ConnectionError:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        data["detail"] = "Unable to connect to webvirtd"

    return Response(data, status_code)
