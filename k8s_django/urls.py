"""
URL configuration for k8s_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import os
import random

from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import path

node_id: int | None = None


def node_version(request: HttpRequest) -> JsonResponse:
    global node_id
    if node_id is None:
        node_id = random.randint(0x10000000, 0xFFFFFFFF)
    data = {
        'version': os.environ.get('APP_RELEASE'),
        'node': hex(node_id).upper(),
    }
    return JsonResponse(data)


def request_info(request: HttpRequest) -> JsonResponse:
    return JsonResponse(request.headers.__dict__)


def health_check(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz', health_check),
    path('test/node', node_version),
    path('test/headers', request_info),
]
