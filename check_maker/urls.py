"""check_maker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from check_maker.api import views
from check_maker.views import download

router = SimpleRouter()
router.register(r'merchant-points', views.MerchantPointViewSet)
router.register(r'printers', views.PrinterViewSet)
router.register(r'checks', views.CheckViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path:path>/', download, name='media'),
    path('openapi/', get_schema_view(
        title='Check maker API',
        description=_('API microservice for generating checks by orders'),
        public=True,
        version='v1'
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger'),
    path('', include(router.urls))
]
