from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import DatabaseMiddlewareConfig
from .views import TenantAPI, CompanySettingsAPI, CacheAPI, OnboardAPI

app_name = DatabaseMiddlewareConfig.name
router = DefaultRouter()

router.register('', TenantAPI, "TenantAPI")
urlpatterns = [
    path('settings/', CompanySettingsAPI.as_view()),
    path('clear_cache/', CacheAPI.as_view()),
    path('create_super_tenant/', OnboardAPI.as_view()),
]

urlpatterns += router.urls
