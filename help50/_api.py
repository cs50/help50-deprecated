import collections

__all__ = ["HELPERS", "PREPROCESSORS", "Error", "helper", "preprocessor"]

HELPERS = collections.defaultdict(list)
PREPROCESSORS = collections.defaultdict(list)


class Error(Exception):
    pass


def helper(*domains):
    """ Decorator that indicateas that a given function is a helper. """
    def decorator(func):
        for domain in domains:
            HELPERS[domain].append(func)
        return func
    return decorator


def preprocessor(*domains):
    """ Decorator that indicateas that a given function is a preprocessor. """
    def decorator(func):
        for domain in domains:
            PREPROCESSORS[domain].append(func)
        return func
    return decorator
