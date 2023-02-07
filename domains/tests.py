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
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from requests.exceptions import ConnectionError
from rest_framework.response import Response
from rest_framework.test import APIClient


class DomainsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test", password="test")

    @mock.patch("requests_unixsocket.Session")
    def test_get(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        response.json = lambda: []
        session.get.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/")
        data = response.json()
        self.assertEqual(data, [])

    @mock.patch("requests_unixsocket.Session")
    def test_get_connection_error(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        session.get.side_effect = ConnectionError

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/")
        data = response.json()
        self.assertTrue("detail" in data)
        self.assertEqual(data["detail"], "Unable to connect to webvirtd")
        self.assertEqual(response.status_code, 500)


class DomainTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test", password="test")

    @mock.patch("requests_unixsocket.Session")
    def test_get(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        response.json = lambda: {}
        session.get.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/test/")
        data = response.json()
        self.assertEqual(data, {})

    @mock.patch("requests_unixsocket.Session")
    def test_get_connection_error(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        session.get.side_effect = ConnectionError

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/test/")
        data = response.json()
        self.assertTrue("detail" in data)
        self.assertEqual(data["detail"], "Unable to connect to webvirtd")
        self.assertEqual(response.status_code, 500)

    @mock.patch("requests_unixsocket.Session")
    def test_start_post(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=201)
        response.json = lambda: {}
        session.post.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.post("/domains/test/start/")
        self.assertEqual(response.status_code, 201)

    @mock.patch("requests_unixsocket.Session")
    def test_shutdown_post(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        response.json = lambda: {}
        session.post.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.post("/domains/test/shutdown/")
        self.assertEqual(response.status_code, 200)
