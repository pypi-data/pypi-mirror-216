import pickle

import simplejson as json

from redis import Redis, StrictRedis
from django.conf import settings

from tenantclient.utils.thread_container import ThreadContainer

cache_settings = settings.CACHE_SETTINGS
__redis__client__ = StrictRedis(**cache_settings)


class CacheItem(object):

    @staticmethod
    def to_cache_item(item):
        if item is not None:
            cache_item = pickle.loads(item)
            return CacheItem(**cache_item)
        return None

    def __init__(self, cache_key, value_type, value, version, namespace: str):
        self.version = version
        self.cache_key = cache_key
        self.value = value
        self.value_type = value_type
        self.namespace = namespace

    def to_cache(self) -> bytes:
        try:
            dict_repr = {
                "cache_key": self.cache_key,
                "version": self.version,
                "value": self.value,
                "value_type": self.value_type,
                "namespace": self.namespace
            }
            return pickle.dumps(dict_repr)
        except Exception as e:
            print(e)
            raise Exception('value could not be serialized')

    def to_value(self):
        try:
            return self.value
        except Exception as e:
            raise Exception('value could not be serialized')


class Cache(object):
    version = 1.0

    def __init__(self, client: Redis, namespace: str = 'default', **kwargs):
        self.version = Cache.version
        self.client = client
        self.namespace = namespace
        self.request = kwargs.get('request', None)
        self.request_key = None

    @staticmethod
    def get_tenant_id():
        tenant_id = ThreadContainer.get_value("tenant_id")
        return tenant_id if tenant_id is not None else "default"

    def qualified_ns(self):
        if self.namespace == 'default':
            tenant_id = 'default'
        else:
            tenant_id = str(Cache.get_tenant_id())
        return ":".join(["tenant", tenant_id, str(self.namespace)])

    def qualified_key(self, key):
        return ":".join([self.qualified_ns(), str(key)])

    def get_all_keys(self):
        qualified_ns = self.qualified_ns()
        wildcard_qualified_ns = qualified_ns + "*"
        return [key for key in self.client.keys(wildcard_qualified_ns)]

    def get(self, key: str):
        qualified_key = self.qualified_key(key=key)
        cache_item = self.client.get(qualified_key)
        if cache_item is not None:
            cache_item = CacheItem.to_cache_item(cache_item)
            return cache_item.to_value()
        return None

    def get_request_response(self):
        return self.get(self.get_request_key())

    def get_all(self, keys: list):
        return [self.get(key) for key in keys]

    def set(self, key: str, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        """
        qualified_ns = self.qualified_ns()
        cache_item = CacheItem(cache_key=key,
                               value_type='str',
                               value=value,
                               version=Cache.version,
                               namespace=qualified_ns)
        key = self.qualified_key(key=cache_item.cache_key)
        self.client.set(key, cache_item.to_cache(), ex, px, nx, xx, keepttl)

    def get_request_key(self):
        if self.request_key:
            return self.request_key
        if self.request is None:
            raise Exception('no request object found')
        query_params = self.request.query_params
        attrs = [self.request.path, json.dumps(query_params)]
        if 'org_node' not in self.request.query_params:
            user = self.request.user
            attrs.append(str(user.pk))
        self.request_key = ':'.join(attrs)
        return self.request_key

    def set_request_response(self, response, ex=2 * 60 * 60, px=None, nx=False, xx=False, keepttl=False):
        self.set(self.get_request_key(), response, ex, px, nx, xx, keepttl)

    def delete(self, key: str):
        qualified_key = self.qualified_key(key=key)
        self.client.delete(qualified_key)

    def clear_all(self):
        all_keys = self.get_all_keys()
        if len(all_keys) > 0:
            self.client.delete(*self.get_all_keys())

    def lock(self, key):
        return self.client.lock(name=self.qualified_key(key), blocking_timeout=10, thread_local=False)


class CacheService(object):

    @staticmethod
    def default_cache():
        return Cache(client=__redis__client__, namespace='default')

    @staticmethod
    def tenant_cache():
        return Cache(client=__redis__client__, namespace="tenant")

    @staticmethod
    def products():
        return Cache(client=__redis__client__, namespace="products")

    @staticmethod
    def auth_token():
        return Cache(client=__redis__client__, namespace="auth_token")

    @staticmethod
    def nodes():
        return Cache(client=__redis__client__, namespace="nodes")

    @staticmethod
    def beats():
        return Cache(client=__redis__client__, namespace="beats")

    @staticmethod
    def users():
        return Cache(client=__redis__client__, namespace="users")

    @staticmethod
    def requests(request=None):
        return Cache(client=__redis__client__, namespace="requests", request=request)

    @staticmethod
    def custom_keys():
        return Cache(client=__redis__client__, namespace="custom_key")

    @staticmethod
    def clear_keys_for_group(group: str, key_sub_str: str, **kwargs):
        cache = getattr(CacheService, group)()
        c_keys = cache.client.keys("*{}:{}*".format(group, key_sub_str))
        if len(c_keys) > 0:
            cache.client.delete(*c_keys)
        return '{} keys deleted'.format(len(c_keys))


def execute_with_cache(cache: Cache, key: str, value_retriever):
    value = cache.get(key)
    if value is not None:
        return value
    if value_retriever is not None:
        value = value_retriever()
        cache.set(key, value)
    return value
