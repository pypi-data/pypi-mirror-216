"""Assorted utility functions."""

import collections
from contextlib import contextmanager
import math
import signal
import sys
import types
import typing

import decorator

sqrt2 = math.sqrt(2)

def cached(oldMethod):
    """Decorator for making a method with no arguments cache its result"""
    storageName = f'_cached_{oldMethod.__name__}'
    @decorator.decorator
    def wrapper(wrapped, *args, **kwargs):
        self = args[0]
        try:
            # Use __getattribute__ for direct lookup in case self is a Distribution
            return self.__getattribute__(storageName)
        except AttributeError:
            value = wrapped(self)
            setattr(self, storageName, value)
            return value
    return wrapper(oldMethod)

def cached_property(oldMethod):
    return property(cached(oldMethod))

def argsToString(args, kwargs={}):
    args = ', '.join(repr(arg) for arg in args)
    kwargs = ', '.join(f'{name}={value!r}' for name, value in kwargs.items())
    parts = []
    if args:
        parts.append(args)
    if kwargs:
        parts.append(kwargs)
    return ', '.join(parts)

@contextmanager
def alarm(seconds, handler=None, noNesting=False):
    if seconds <= 0 or not hasattr(signal, 'SIGALRM'):  # SIGALRM not supported on Windows
        yield
        return
    if handler is None:
        handler = signal.SIG_IGN
    signal.signal(signal.SIGALRM, handler)
    if noNesting:
        assert oldHandler is signal.SIG_DFL, 'SIGALRM handler already installed'
    length = int(math.ceil(seconds))
    previous = signal.alarm(length)
    if noNesting:
        assert previous == 0, 'nested call to "alarm"'
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

class DefaultIdentityDict:
    """Dictionary which is the identity map by default.

    The map works on all objects, even unhashable ones, but doesn't support all
    of the standard mapping operations.
    """
    def __init__(self):
        self.storage = {}

    def clear(self):
        self.storage.clear()

    def __getitem__(self, key):
        return self.storage.get(id(key), key)

    def __setitem__(self, key, value):
        self.storage[id(key)] = value

    def __contains__(self, key):
        return id(key) in self.storage

    def __repr__(self):
        pairs = (f'{hex(key)}: {value!r}' for key, value in self.storage.items())
        allPairs = ', '.join(pairs)
        return f'<DefaultIdentityDict {{{allPairs}}}>'

# Generic type introspection functions backported to Python 3.7
# (code taken from their Python 3.8 implementations)

def get_type_origin(tp):
    """Version of `typing.get_origin` supporting Python 3.7."""
    assert sys.version_info >= (3, 7)
    if sys.version_info >= (3, 8):
        return typing.get_origin(tp)
    if isinstance(tp, typing._GenericAlias):
        return tp.__origin__
    if tp is typing.Generic:
        return typing.Generic
    return None

def get_type_args(tp):
    """Version of `typing.get_args` supporting Python 3.7."""
    assert sys.version_info >= (3, 7)
    if sys.version_info >= (3, 8):
        return typing.get_args(tp)
    if isinstance(tp, typing._GenericAlias) and not tp._special:
        res = tp.__args__
        if get_type_origin(tp) is collections.abc.Callable and res[0] is not Ellipsis:
            res = (list(res[:-1]), res[-1])
        return res
    return ()

# Patched version of typing.get_type_hints fixing bpo-37838

if (sys.version_info >= (3, 8, 1)
    or (sys.version_info < (3, 8) and sys.version_info >= (3, 7, 6))):
    get_type_hints = typing.get_type_hints
else:
    def get_type_hints(obj, globalns=None, localns=None):
        if not isinstance(obj, (type, types.ModuleType)) and globalns is None:
            wrapped = obj
            while hasattr(wrapped, '__wrapped__'):
                wrapped = wrapped.__wrapped__
            globalns = getattr(wrapped, '__globals__', {})
        return typing.get_type_hints(obj, globalns, localns)
