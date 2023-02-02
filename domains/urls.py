"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path

from . import views

urlpatterns = [
    path("domains/", views.domains),
    path("domains/<str:name>/", views.domain),
    path("domains/<str:name>/start/", views.domain_start),
    path("domains/<str:name>/shutdown/", views.domain_shutdown),
]
