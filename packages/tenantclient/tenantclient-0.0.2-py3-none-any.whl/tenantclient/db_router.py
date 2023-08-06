from django.db import transaction, DEFAULT_DB_ALIAS, connections


from .constants import TENANT_DB_CONNECTION, TENANT_ID
from django.conf import settings

from .utils.thread_container import ThreadContainer


class DbRouter:
    """
    A router to control all database operations on models.
    """

    def db_for_read(self, model, **hints):
        threadContainer = ThreadContainer()
        connection_name = threadContainer.get_value(TENANT_ID)
        if connection_name and connection_name not in settings.DATABASES:
            connection_config = threadContainer.get_value(TENANT_DB_CONNECTION)
            settings.DATABASES[connection_name] = connection_config
        return connection_name

    def db_for_write(self, model, **hints):
        threadContainer = ThreadContainer()
        connection_name = threadContainer.get_value(TENANT_ID)
        if connection_name and connection_name not in settings.DATABASES:
            connection_config = threadContainer.get_value(TENANT_DB_CONNECTION)
            settings.DATABASES[connection_name] = connection_config
        return connection_name

    def __init__(self):
        def get_connection(using=None):
            if using is None:
                tenant_id = ThreadContainer.get_value(TENANT_ID)
                if tenant_id is None:
                    using = DEFAULT_DB_ALIAS
                else:
                    using = tenant_id
            return connections[using]

        transaction.get_connection = get_connection
