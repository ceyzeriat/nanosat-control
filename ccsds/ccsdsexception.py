#!/usr/bin/env python
# -*- coding: utf-8 -*-


def doraise(obj, **kwargs):
    return bool(kwargs.pop('raiseError', getattr(obj, 'raiseError', True)))


def raise_it(exc, raiseoupas, *args, **kwargs):
    exc = exc(*args, **kwargs)
    if raiseoupas:
        raise exc
    else:
        print("\033[31m{}\033[39m".format(exc.message))
        return True
    return False


class CCSDSException(Exception):
    """
    Root for CCSDS Exceptions
    """
    def _init(self, *args, **kwargs):
        self.args = [a for a in args] + [a for a in kwargs.values()]

    def __repr__(self):
        return repr(self.message)

    __str__ = __repr__


class TruncatedPrimaryHeader(CCSDSException):
    """
    The packet has its primary header truncated
    """
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        self.message = "The packet has its primary header truncated"

class TruncatedSecondaryHeader(CCSDSException):
    """
    The packet has its primary header truncated
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "The packet '{}' has its"\
                       "secondary header truncated".format(name)

class TruncatedData(CCSDSException):
    """
    The packet has its data truncated
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "The packet '{}' has its data truncated".format(name)

class NoSuchKey(CCSDSException):
    """
    Missing key in the dictionary
    """
    def __init__(self, dic, key, *args, **kwargs):
        self._init(dic, key, *args, **kwargs)
        self.message = "No key '{}' in dict '{}'".format(key, dic)
