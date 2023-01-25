"""Copyright (C) 2023 Kevin Morris"""
import json
from urllib.parse import quote_plus

import requests_unixsocket
from django.conf import settings
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
        response = session.post(
            f"http+unix://{uri}/domains",
            data=json.dumps({"user": user}),
        )
        return Response(response.json())
