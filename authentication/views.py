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
from http import HTTPStatus

import pam
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class AuthView(APIView):
    def __init__(self, *args, **kwargs) -> "AuthView":
        super().__init__(*args, **kwargs)
        self.pam = pam.PamAuthenticator()

    def post(self, request: Request) -> Response:
        username = request.data.get("user", str())
        password = request.data.get("password", str())

        if not self.pam.authenticate(username, password, service="login"):
            return Response(
                {"detail": "Unrecognized user/password combination"},
                status=HTTPStatus.UNAUTHORIZED,
            )

        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.create_user(
                username=username, password=password
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTPStatus.OK,
        )
