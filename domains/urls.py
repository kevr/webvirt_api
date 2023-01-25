"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path

from .views import DomainsView

urlpatterns = [
    path("domains/", DomainsView.as_view()),
]
