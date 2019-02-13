import functools


class ProxyMeta(type):
    """A class that other classes can use as a meta clas to allow the use of a socks proxy."""
    def __call__(cls, *args, **kwargs):
        cls.proxies = kwargs.pop('proxies', None)
        return type.__call__(cls, *args, **kwargs)
