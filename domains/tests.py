"""Copyright (C) 2023 Kevin Morris"""
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
        session.post.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/")
        data = response.json()
        self.assertEqual(data, [])

    @mock.patch("requests_unixsocket.Session")
    def test_get_connection_error(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        response.json = lambda: []
        session.post.side_effect = ConnectionError

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
        session.post.return_value = response

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/test/")
        data = response.json()
        self.assertEqual(data, {})

    @mock.patch("requests_unixsocket.Session")
    def test_get_connection_error(self, mock: mock.MagicMock):
        session = mock.return_value

        response = Response(status=200)
        response.json = lambda: []
        session.post.side_effect = ConnectionError

        self.client.force_authenticate(self.user)
        response = self.client.get("/domains/test/")
        data = response.json()
        self.assertTrue("detail" in data)
        self.assertEqual(data["detail"], "Unable to connect to webvirtd")
        self.assertEqual(response.status_code, 500)
