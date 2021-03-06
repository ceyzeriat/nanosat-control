#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 2016-2017  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################


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
        self.message = "Blob too small, could not grab '{}', "\
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
    If the key has both a dic and a fctpack/fctunpack
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Should assign either a dic or a fctpack/fctunpack, "\
                       "in '{}'".format(name)


class BadTypeDefinition(CCSDSException):
    """
    If the type given in unknown
    """
    def __init__(self, typ, name, *args, **kwargs):
        self._init(typ, name, *args, **kwargs)
        self.message = "Unknown type '{}' for '{}'".format(typ, name)


class NoDic(CCSDSException):
    """
    If the ccsdskey is defined through fctpack/unpack and not a dic
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "CCSDS key '{}' is defined through fctpack/unpack, "\
                       "not dic".format(name)


class PacketValueMissing(CCSDSException):
    """
    If at packing, a value is missing
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "CCSDS value for key '{}' is not optional".format(name)


class CategoryMissing(CCSDSException):
    """
    Packet category does not exist
    """
    def __init__(self, cat, pld, *args, **kwargs):
        self._init(cat, pld, *args, **kwargs)
        self.message = "Packet category '{}' with payload flag '{}' does "\
                       "not exist".format(cat, pld)


class WrongCategoryTableName(CCSDSException):
    """
    Category has wrong name format
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Category '{}' is not valid. Should be "\
                       "underscorded-lower-plural".format(name)


class WrongCategoryObjectName(CCSDSException):
    """
    Category has wrong name format
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Category '{}' is not valid. Should be "\
                       "Capitalized-Camelcase-singular".format(name)


class DuplicateKeyName(CCSDSException):
    """
    Names in a trousseau must be unique
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Name '{}' is duplicated in the trousseau".format(name)


class WrongNameFormat(CCSDSException):
    """
    Forbidden characters in the category name
    """
    def __init__(self, name, *args, **kwargs):
        self._init(name, *args, **kwargs)
        self.message = "Invalid name '{}' for category".format(name)


class PIDMissing(CCSDSException):
    """
    PID does not exist
    """
    def __init__(self, pid, *args, **kwargs):
        self._init(pid, *args, **kwargs)
        self.message = "PID '{}' does not exist".format(pid)


class InvalidListOfBits(CCSDSException):
    """
    If user required non-octet with listof modes
    """
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        self.message = "Cannot do listof mode with non-octets"


class InvalidMetaTrousseauKey(CCSDSException):
    """
    If the meta-trousseau key is unknown
    """
    def __init__(self, key, *args, **kwargs):
        self._init(key, *args, **kwargs)
        self.message = "Meta-Trousseau Key '{}' does not exist".format(key)


class NoMetaTrousseauAttribute(CCSDSException):
    """
    If one tries to access a trousseau attribute on a meta-trousseau
    """
    def __init__(self, key, *args, **kwargs):
        self._init(key, *args, **kwargs)
        self.message = "Attribute '{}' does not exist for meta-trousseau"\
                        .format(key)


class WrongAt(CCSDSException):
    """
    If the delay parameter at is not understood
    """
    def __init__(self, at, *args, **kwargs):
        self._init(at, *args, **kwargs)
        self.message = "Delay paramter at '{}' is not valid".format(at)
