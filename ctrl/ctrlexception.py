#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CTRLException(Exception):
    """
    Root for CTRL Exceptions
    """
    def _init(self, *args, **kwargs):
        self.args = [a for a in args] + [a for a in kwargs.values()]

    def __repr__(self):
        return repr(self.message)

    __str__ = __repr__

class ReadOnly(CTRLException):
    """
    Read-only
    """
    def __init__(self, key, *args, **kwargs):
        self._init(key, *args, **kwargs)
        self.message = "Attribute '{}' is read-only".format(key)

class NoSuchKey(CTRLException):
    """
    Missing key in the parameter dictionary
    """
    def __init__(self, param, key, *args, **kwargs):
        self._init(param, key, *args, **kwargs)
        self.message = "No key '{}' in param '{}'".format(key, param)