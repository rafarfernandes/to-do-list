from django.core.cache import cache

def set_to_cache(key, value, timeout=None):

    cache.set(key, value, timeout=timeout)

def get_from_cache(key):

    return cache.get(key)
