"""
URL configuration for etherbeing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.base.controllers import GithubViewSet
from django.conf import settings

router = DefaultRouter()
router.register("", GithubViewSet, "github")

urlpatterns = [
    path("api/", include((router.urls, "api"), namespace="v1")),
]
if settings.DEBUG:
    urlpatterns.insert(0, path("admin/", admin.site.urls)) # DO NOT ALLOW admin panel access from the production site
