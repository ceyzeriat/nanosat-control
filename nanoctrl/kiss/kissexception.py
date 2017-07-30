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


class KISSException(Exception):
    """
    Root for KISS Exceptions
    """
    def _init(self, *args, **kwargs):
        self.args = [a for a in args] + [a for a in kwargs.values()]

    def __repr__(self):
        return repr(self.message)

    __str__ = __repr__


class BadCallsignError(KISSException):
    """
    Bad Callsign
    """
    def __init__(self, cs, *args, **kwargs):
        self._init(cs, *args, **kwargs)
        self.message = "Could not extract callsign from '{}'".format(cs)

class SocketClosetError(Exception):
    """
    Socket Closed
    """
    def __init__(self, cs, *args, **kwargs):
        self._init(cs, *args, **kwargs)
        self.message = "Could not extract callsign from '{}'".format(cs)
