"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path

from .views import DomainsView, DomainView, domain_shutdown, domain_start

urlpatterns = [
    path("domains/", DomainsView.as_view()),
    path("domains/<str:name>/", DomainView.as_view()),
    path("domains/<str:name>/start/", domain_start),
    path("domains/<str:name>/shutdown/", domain_shutdown),
]
