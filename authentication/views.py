"""Copyright (C) 2023 Kevin Morris"""
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
