from flask_cache import Cache

cache = Cache()


class CACHE_KEYS(object):
    """
    if not using the cache view-decorator, but instead the .set()
    we need to specify the name of the key.
    list the names here as class variables, to avoid typos
    """
    default_key = 'default_key'


def invalidate_cache():
    cache.clear()