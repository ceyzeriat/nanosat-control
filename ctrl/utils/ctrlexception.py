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

class MissingDBServerFile(CTRLException):
    """
    If the DB server file is missing
    """
    def __init__(self, f, *args, **kwargs):
        self._init(f, *args, **kwargs)
        self.message = "Cannot find DB server file '{}'".format(f)

class NoDBConnection(CTRLException):
    """
    If the DB is not running
    """
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        self.message = "No DB connection open"

class BrokenTelemetryDumpFolder(CTRLException):
    """
    If the Telemetry data dump folder does not exist
    """
    def __init__(self, f, *args, **kwargs):
        self._init(f, *args, **kwargs)
        self.message = "Folder '{}' for telemetry-dump missing".format(f)



# not used
class NoSuchKey(CTRLException):
    """
    Missing key in the parameter dictionary
    """
    def __init__(self, param, key, *args, **kwargs):
        self._init(param, key, *args, **kwargs)
        self.message = "No key '{}' in param '{}'".format(key, param)