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

class CommProcessDead(CTRLException):
    """
    If the communication process is not running
    """
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
        self.message = "The comm process is not running"

class PacketFileMissing(CTRLException):
    """
    If the packet file sent through the socket is missing
    """
    def __init__(self, f, *args, **kwargs):
        self._init(f, *args, **kwargs)
        self.message = "The packet file '{}' does not exist".format(f)

class PacketMismatch(CTRLException):
    """
    If the packet file content is different from the data obtained
    through the socket
    """
    def __init__(self, f, *args, **kwargs):
        self._init(f, *args, **kwargs)
        self.message = "Mismatch between the data in file '{}' and the data"\
                       "obtained through socket".format(f)

class UnknownAntenna(CTRLException):
    """
    Antenna keyword not known
    """
    def __init__(self, antenna, *args, **kwargs):
        self._init(antenna, *args, **kwargs)
        self.message = "Antenna keyword '{}' unknown".format(antenna)


# not used
class NoSuchKey(CTRLException):
    """
    Missing key in the parameter dictionary
    """
    def __init__(self, param, key, *args, **kwargs):
        self._init(param, key, *args, **kwargs)
        self.message = "No key '{}' in param '{}'".format(key, param)