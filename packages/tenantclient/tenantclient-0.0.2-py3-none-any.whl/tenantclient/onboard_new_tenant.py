from django.contrib.auth.models import Permission

from django.db import transaction

from .utils.thread_container import ThreadContainer
from .constants import TENANT_ID, TENANT_DB_CONNECTION, TENANT
from .models import TenantInfo
from datetime import datetime


class OnboardTenant(object):
    def __init__(self, tenant_id: str, user_id: str, name, password, mobile_number, **extra_fields):
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.name = name
        self.password = password
        self.user_extra = extra_fields
        self.user_extra['mobile_number'] = mobile_number
        self.user_extra['date_joined'] = datetime.utcnow()
        self.tenant = TenantInfo.objects.get(tenant_id=self.tenant_id)

    def set_tenant(self):
        ThreadContainer.clear()
        tenant = TenantInfo.objects.filter(tenant_id=self.tenant_id).first()
        config = {'ENGINE': tenant.engine,
                  'NAME': tenant.database,
                  'USER': tenant.user,
                  'PASSWORD': tenant.password,
                  'HOST': tenant.host,
                  'PORT': tenant.port,
                  # 'ATOMIC_REQUESTS': True
                  }
        ThreadContainer.set_value(TENANT_ID, tenant.tenant_id)
        ThreadContainer.set_value(TENANT_DB_CONNECTION, config)
        ThreadContainer.set_value(TENANT, tenant)

    def create_super_user(self):
        self.set_tenant()
        with transaction.atomic():
            # role.objects.filter(tenant_id=self.tenant_id).delete()
            # location.objects.filter(tenant_id=self.tenant_id).delete()
            # TenantGroup.objects.filter(tenant_id=self.tenant_id).delete()
            #
            # super_location = location()
            # super_location.tenant_id = self.tenant_id
            # super_location.using = self.tenant_id
            # super_location.name = 'Super Geographical Location'
            # super_location.save()
            #
            # super_place = place_data()
            # super_place.tenant_id = self.tenant_id
            # super_place.name = 'Super Place'
            # super_place.type = super_location
            # super_place.save_without_historical_record()
            #
            # super_role = role()
            # super_role.tenant_id = self.tenant_id
            # super_role.name = 'ADMIN'
            # super_role.location = super_location
            # super_role.save()
            #
            # super_group = TenantGroup()
            # super_group.name = self.tenant.name + ' ADMIN'
            # super_group.tenant_id = self.tenant_id
            # perms = Permission.objects.all().exclude(codename__regex='tenant')
            # super_group.save()
            # super_group.permissions.set(perms)
            #
            # super_user = employ.objects.create_user(self.user_id, self.name, super_role.id, super_place.id, self.password, **self.user_extra)
            # super_user.tenant_id = self.tenant_id
            # super_user.groups.add(super_group)
            pass
