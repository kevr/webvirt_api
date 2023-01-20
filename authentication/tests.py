"""Copyright (C) 2023 Kevin Morris"""
import json
from http import HTTPStatus
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class AuthTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @mock.patch("pam.PamAuthenticator")
    def test_post(self, pam: mock.MagicMock) -> None:
        # No users exist yet
        self.assertEqual(User.objects.count(), 0)

        instance = pam.return_value
        instance.authenticate.return_value = True

        data = json.dumps({"user": "test", "password": "test_password"})
        response = self.client.post(
            "/auth/", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Assert that a record with the username we gave was created
        record = User.objects.filter(username="test").first()
        self.assertTrue(record is not None)

        # Assert data response expectations:
        # {
        #   "user": "<username>",
        #   "access": "<access_token>",
        #   "refresh": "<refresh_token>",
        # }
        data = response.json()
        self.assertTrue("user" in data and data.get("user") == "test")
        self.assertTrue("access" in data and data.get("access") is not None)
        self.assertTrue("refresh" in data and data.get("refresh") is not None)

    @mock.patch("pam.PamAuthenticator")
    def test_post_existing_user_record(self, pam: mock.MagicMock) -> None:
        User.objects.create_user(username="test", password="test_password")

        # Assert that the user we created is the only user we can find
        self.assertEqual(User.objects.count(), 1)

        instance = pam.return_value
        instance.authenticate.return_value = True

        data = json.dumps({"user": "test", "password": "test_password"})
        response = self.client.post(
            "/auth/", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Assert that we can still only find one user in the database
        # since the user we created was used for authentication
        self.assertEqual(User.objects.count(), 1)

    @mock.patch("pam.PamAuthenticator")
    def test_post_unauthorized(self, pam: mock.MagicMock) -> None:
        instance = pam.return_value
        instance.authenticate.return_value = False

        data = json.dumps({"user": "test", "password": "test_password"})
        response = self.client.post(
            "/auth/", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
