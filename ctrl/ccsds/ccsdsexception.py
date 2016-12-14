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
    def __init__(self, name, key, *args, **kwargs):
        self._init(name, key, *args, **kwargs)
        self.message = "No key '{}' in dict '{}'".format(key, name)

class NoSuchValue(CCSDSException):
    """
    Missing value in the dictionary
    """
    def __init__(self, name, value, *args, **kwargs):
        self._init(name, value, *args, **kwargs)
        self.message = "No value '{}' in dict '{}'".format(value, name)

class NoAbsGrab(CCSDSException):
    """
    If relative grabing is not possible
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Can only parse bits in relatively in '{}'".format(name)

class GrabFail(CCSDSException):
    """
    If the grab mechanism fails to grab as many bits as required
    """
    def __init__(self, name, l, *args, **kwargs):
        self._init(name, l, *args, **kwargs)
        self.message = "Blob too small, could not grab '{}' bits, "\
                       "in '{}'".format(l, name)

class CantApplyOffset(CCSDSException):
    """
    If relative grabing is not possible
    """
    def __init__(self, name, start, offset, *args, **kwargs):
        self._init(name, start, offset, *args, **kwargs)
        self.message = "Cannot apply offset '{}' with start index "\
                       "'{}' in '{}'".format(start, offset, name)

class BadDefinition(CCSDSException):
    """
    If the key has both a dic and a fct/fctrev
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Should assign either a dic or a fct/fctrev "\
                       "'{}'".format(name)

class DecodeOnly(CCSDSException):
    """
    If trying to render while fctrev was not provided
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Cannot render the bits, fctrev was not "\
                       "provided, in '{}'".format(name)

class NoDic(CCSDSException):
    """
    If the ccsdskey is defined through a fct and not a dic
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "CCSDS key '{}' is defined through fct, "\
                       "not dic".format(name)