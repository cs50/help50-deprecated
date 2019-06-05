import collections
import functools

HELPERS = collections.defaultdict(set)

def helper(domain):
    def decorator(func):
        HELPERS[domain].add(func)
        return func
    return decorator


PRE_HELPERS = collections.defaultdict(list)
def pre_helper(domain):
    def decorator(func):
        PRE_HELPERS[domain].append(func)
        return func
    return decorator
