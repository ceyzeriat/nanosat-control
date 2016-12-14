#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CMDException(Exception):
    """
    Root for CMD Exceptions
    """
    def _init(self, *args, **kwargs):
        self.args = [a for a in args] + [a for a in kwargs.values()]

    def __repr__(self):
        return repr(self.message)

    __str__ = __repr__

class ReadOnly(CMDException):
    """
    Read-only
    """
    def __init__(self, key, *args, **kwargs):
        self._init(key, *args, **kwargs)
        self.message = "Attribute '{}' is read-only".format(key)

class NotImplemented(CMDException):
    """
    Not implemented
    """
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        self.message = "Not implemented"

class MissingCommandInput(CMDException):
    """
    Missing input at command call
    """
    def __init__(self, cmd, param, *args, **kwargs):
        self._init(cmd, param, *args, **kwargs)
        self.message = "Parameter '{}' is not optionnal in CMD "\
                       "'{}'".format(param, cmd)

class WrongParamCount(CMDException):
    """
    Missing input at command call
    """
    def __init__(self, cmd, n, *args, **kwargs):
        self._init(cmd, n, *args, **kwargs)
        self.message = "Command '{}' should have '{}' param".format(cmd, n)

class UnknownFormat(CMDException):
    """
    Unknown format
    """
    def __init__(self, fmt, *args, **kwargs):
        self._init(fmt, *args, **kwargs)
        self.message = "Unknown format '{}'".format(fmt)

class MissingFormatInput(CMDException):
    """
    Input missing in format definition
    """
    def __init__(self, fmt, inp, *args, **kwargs):
        self._init(fmt, inp, *args, **kwargs)
        self.message = "Input '{}' is not optional for format "\
                       "'{}'".format(inp, fmt)

class WrongFormatBitLength(CMDException):
    """
    Wrong bit length in format definition
    """
    def __init__(self, fmt, le, *args, **kwargs):
        self._init(fmt, le, *args, **kwargs)
        self.message = "Bits length '{}' is not valid for format "\
                       "'{}'".format(le, fmt)

class WrongParameterDefinition(CMDException):
    """
    If a param of a command is badly defined
    """
    def __init__(self, cmd, par, *args, **kwargs):
        self._init(cmd, par, *args, **kwargs)
        self.message = "Bad parameter definition '{}', in "\
                       "CMD '{}'".format(par, cmd)

class InvalidParameterValue(CMDException):
    """
    Missing input at command call
    """
    def __init__(self, cmd, value, *args, **kwargs):
        self._init(cmd, value, *args, **kwargs)
        self.message = "Value '{}' is not valid for parameter "\
                       "'{}'".format(value, cmd)
