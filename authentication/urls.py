"""Copyright (C) 2023 Kevin Morris"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthView

urlpatterns = [
    path("auth/", AuthView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
]
