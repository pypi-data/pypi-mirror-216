from django.core import serializers
from django.template.response import TemplateResponse
from rest_framework import status

from .services.cache_service import CacheService
from .utils.thread_container import ThreadContainer

from .models import TenantInfo
from .constants import TENANT_ID, TENANT_DB_CONNECTION, TENANT
from django.urls import resolve


def set_tenant(tenant):
    # config = {'ENGINE': tenant.engine,
    #           'NAME': tenant.database,
    #           'USER': tenant.user,
    #           'PASSWORD': tenant.password,
    #           'HOST': tenant.host,
    #           'PORT': tenant.port,
    #           # 'ATOMIC_REQUESTS': True
    #           }
    ThreadContainer.set_value(TENANT_ID, tenant)
    # ThreadContainer.set_value(TENANT_DB_CONNECTION, config)
    # ThreadContainer.set_value(TENANT, tenant)


def clear_tenant():
    ThreadContainer.clear()


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.flag = True

    @staticmethod
    def set_tenant_cache(tenant: TenantInfo):
        CacheService.default_cache().set(tenant.tenant_id, serializers.serialize("json", [tenant, ]))

    @staticmethod
    def clear_tenant_cache(tenant_id=None):
        if tenant_id:
            CacheService.default_cache().delete(tenant_id)
        else:
            CacheService.default_cache().clear_all()

    @staticmethod
    def get_tenant_cache(tenant_id: str) -> TenantInfo:
        tenant = None
        tenant_json = CacheService.default_cache().get(tenant_id)
        if tenant_json is not None:
            for __tenant in serializers.deserialize("json", tenant_json):
                tenant = __tenant.object
        return tenant

    @classmethod
    def retrieve_tenant(cls, request):
        tenant_id = 'default'  # remove default after complete setup
        # tenant_id = request.META.get('HTTP_TENANT_ID')
        if tenant_id is None or tenant_id == 'None':
            if request.method == 'GET':
                path = request.path
                try:
                    func, args, kwargs = resolve(path)
                    tenant_id = kwargs.get(TENANT_ID)

                except Exception as e:
                    print(e)
        if tenant_id is None:
            tenant_id = request.COOKIES.get('tenant_id')
        if request.path in ['/whatsapp/webhook/']:
            tenant_id = 'brinton'
        if tenant_id in [None, 'None'] and request.path in ['/hotline/get_delivery_reports/',
                                                            '/reports/get_order_reports/',
                                                            '/whatsapp/webhook/']:
            tenant_id = 'glenmark'
        if tenant_id:
            # tenant = cls.get_tenant_cache(tenant_id)
            # if tenant is None:
            #     tenant = TenantInfo.objects.filter(tenant_id=tenant_id).first()
            #     if tenant:
            #         cls.set_tenant_cache(tenant)
            # return tenant
            return tenant_id  # changed to return only id as other services doesn't require tenant info

    def process_request(self, request):
        if self.flag:
            tenant = TenantMiddleware.retrieve_tenant(request)

            if tenant is None:
                # func, args, kwargs = resolve(request.path)
                # identifier = kwargs.get(IDENTIFIER)
                # if identifier:
                #     url = TinyUrl.objects.get(identifier=identifier)
                #     return True
                # if request.method == 'GET' and request.path in ['/employee/mobile/register/',
                #                                                 '/employee/mobile/login/',
                #                                                 '/whatsapp/webhook/']:
                #     return True
                return False

            set_tenant(tenant)
            return True

    def __call__(self, request):
        should_continue = self.process_request(request=request)
        response = (self.get_response(request) if should_continue else
                    TemplateResponse(request, 'tenantclient/tenant_form.html',
                                     status=status.HTTP_402_PAYMENT_REQUIRED).render())
        if should_continue:
            response.set_cookie('tenant_id', ThreadContainer.get_value(TENANT_ID))
        clear_tenant()
        return response
