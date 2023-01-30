"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path

from .views import DomainsView, DomainView

urlpatterns = [
    path("domains/", DomainsView.as_view()),
    path("domains/<str:name>/", DomainView.as_view()),
]
