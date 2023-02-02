"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path

from . import views

urlpatterns = [
    path("domains/", views.http_request),
    path("domains/<str:name>/", views.http_request),
    path("domains/<str:name>/start/", views.http_request),
    path("domains/<str:name>/shutdown/", views.http_request),
]
