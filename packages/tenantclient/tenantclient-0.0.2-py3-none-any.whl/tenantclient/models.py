from django.db import models

from .mixins import (TenantModelMixin)
from .utils.tenant_utils import (
    get_current_tenant,
    get_current_tenant_value, set_object_tenant
)


class TenantManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        # Injecting tenant_id filters in the get_queryset.
        # Injects tenant_id filter on the current model for all the non-join/join queries.
        current_tenant = get_current_tenant()
        queryset = super().get_queryset().filter(tenant_id=current_tenant)

        return queryset

    def bulk_create(self, objs, **kwargs):
        if get_current_tenant():
            tenant_value = get_current_tenant_value()
            for obj in objs:
                set_object_tenant(obj, tenant_value)

        return super(TenantManager, self).bulk_create(objs, **kwargs)


class TenantModel(TenantModelMixin, models.Model):
    # Abstract model which all the models related to tenant inherit.
    tenant_id = models.CharField(max_length=255, null=True, blank=True)
    objects = TenantManager()

    class Meta:
        abstract = True
        base_manager_name = 'objects'


class TenantInfo(models.Model):
    engine_choices = (('django.db.backends.mysql', 'MYSQL'),)
    tenant_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    referrer_id = models.CharField(max_length=255, unique=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=3306)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    database = models.CharField(max_length=255)
    engine = models.CharField(max_length=255, choices=engine_choices)
    settings = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenant_info'
        abstract = True
        permissions = (
            ("change_company_settings", "Can Change Company Settings"),
            ("view_company_settings", "Can View Company Settings"),
        )

    def __str__(self):
        return self.tenant_id
