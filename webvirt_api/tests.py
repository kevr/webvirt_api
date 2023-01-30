from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from .middleware import CorsMiddleware


class CorsMiddlewareTest(TestCase):
    def test_middleware(self):
        pass

    def test_access_control_request_method(self):
        request = HttpRequest()
        request.method = "OPTIONS"
        request.META = {"HTTP_ACCESS_CONTROL_REQUEST_METHOD": True}

        mw = CorsMiddleware(lambda x: HttpResponse())
        response = mw(request)
        self.assertTrue("Content-Length" in response)
        self.assertTrue("Access-Control-Max-Age" in response)

    def test_access_control_allow_origin(self):
        test_origin = "http://testserver"

        origins = settings.CORS_ALLOWED_ORIGINS
        settings.CORS_ALLOWED_ORIGINS = [test_origin]

        request = HttpRequest()
        request.method = "POST"
        request.headers = {"Origin": test_origin}

        mw = CorsMiddleware(lambda x: HttpResponse())
        response = mw(request)
        self.assertTrue("Access-Control-Allow-Origin" in response)
        self.assertEqual(response["Access-Control-Allow-Origin"], test_origin)
        settings.CORS_ALLOWED_ORIGINS = origins
