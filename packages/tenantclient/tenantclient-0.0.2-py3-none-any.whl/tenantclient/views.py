# Create your views here.
import json
import logging
import os

from django.contrib.auth.decorators import permission_required
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.conf import settings as SETTINGS
from .services.cache_service import CacheService
from .utils.thread_container import ThreadContainer
from .constants import TENANT
from .models import TenantInfo
from .serializers import TenantSerializer, TenantSettingsSerializer
from .tenant_manager import TenantMiddleware


class TenantAPI(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    authentication_classes = [TokenAuthentication]
    serializer_class = TenantSerializer
    # permission_classes = [IsSuperUser]

    def get_queryset(self):
        return TenantInfo.objects.all()


class CompanySettingsAPI(APIView):
    """
    change to generic viewset to update tenant data in db
    """
    authentication_classes = [TokenAuthentication]
    serializer_class = TenantSettingsSerializer

    def get(self, request):
        tenant = ThreadContainer.get_value(TENANT)
        serializer = self.serializer_class(tenant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(('tenantclient.change_company_settings',), raise_exception=True))
    def put(self, request, *args, **kwargs):
        """
        change to generic viewset to update tenant data in db
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # request_data = request.data
        # file = request_data.get('file', None)
        # data = request_data.get('data', None)
        # data = data if type(data) == dict else json.loads(data)
        # tenant: TenantInfo = TenantInfo.objects.get(pk=ThreadContainer.get_value(TENANT).id)
        # old_data = tenant.settings
        # old_data.update(data['settings'])
        # data['settings'] = old_data
        # if file is not None:
        #     extension = str(file).split('.')[-1]
        #     # s3_file_url = self.upload_get_url(file=file, extension=extension)
        #     data['settings'].update({'image_name': str(s3_file_url)})
        # # if 'company_name' not in data['settings']:
        # #     data['settings'].update({'company_name': tenant.name})
        # # if 'onboard_alternate_otp_flag' not in data['settings']:
        # #     data['settings'].update({'onboard_alternate_otp_flag': False})
        # # if 'is_otp_allowed' not in data['settings']:
        # #     data['settings'].update({'is_otp_allowed': True})
        # # if 'contact_number_length' not in data['settings']:
        # #     data['settings'].update({'contact_number_length': 10})
        # if 'salesman_hotline_msg' not in data['settings']:
        #     data['settings'].update({'salesman_hotline_msg': "Hi, I'm your area " + str(
        #         tenant.name) + "Representative. Please order Products at the below link- "
        #                        "https://api.adjoint.co/hotline/" + str(
        #         tenant.tenant_id) + "/?id=##mapping_id##"})
        # # if 'near_by_radius' not in data['settings']:
        # #     data['settings'].update({'near_by_radius': 1000})
        # serializer = self.serializer_class(data=data, instance=tenant)
        # if serializer.is_valid(raise_exception=True):
        #     tenant = serializer.save()
        #     TenantMiddleware.set_tenant_cache(tenant)
        #     CacheService.default_cache().clear_all()
        #     CacheService.default_cache().set(tenant.tenant_id, serializers.serialize("json", [tenant, ]))
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        pass

    # @classmethod
    # def upload_get_url(cls, file, extension):
    #     tenant = ThreadContainer.get_value(TENANT)
    #     client = boto3.client('s3', aws_access_key_id=SETTINGS.AWS_ACCESS_KEY_ID,
    #                           aws_secret_access_key=SETTINGS.AWS_SECRET_ACCESS_KEY)
    #     filename = 'Hotline Logo-{name}.{ext}'.format(name=tenant.name, ext=extension)
    #     fs = FileSystemStorage(location=SETTINGS.TMP_ROOT)
    #     filepath = fs.save(filename, file)
    #     file_path = fs.url(filepath)
    #     file_path = SETTINGS.TMP_ROOT + filename
    #     if len(filename) > 0 and len(file_path) > 0:
    #         try:
    #             client.upload_file(file_path, SETTINGS.S3_BUCKET_NAME, 'Logos/{}'.format(filename))
    #             url = "https://{could_front_domain}/Logos/{filename}".format(
    #                 could_front_domain=SETTINGS.AWS_CLOUD_FRONT_DOMAIN,
    #                 filename=filename)
    #         except FileNotFoundError as e:
    #             logging.error(e)
    #             return None
    #         except NoCredentialsError as e:
    #             logging.error(e)
    #             return None
    #         os.remove(file_path)
    #         return url
    #     return None


class CacheAPI(APIView):
    # permission_classes = [IsSuperUser]
    authentication_classes = [TokenAuthentication]

    def get(self, *args, **kwargs):
        cache.clear()
        return Response('cache cleared', status=status.HTTP_200_OK)


class OnboardAPI(APIView):
    # permission_classes = [IsSuperUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # from tenant_middleware.onboard_new_tenant import OnboardTenant
        # data = request.data
        # # data = json.loads(data)
        # new_tenant = OnboardTenant(tenant_id=data['tenant_id'], user_id=data['user_id'], name=data['name'],
        #                            password=data['password'], mobile_number=data['mobile_number'])
        # new_tenant.create_super_user()
        # return Response('super_user created', status=status.HTTP_200_OK)
        pass
