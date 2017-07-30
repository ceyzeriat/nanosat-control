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



class MGMTException(Exception):
    """
    Root for CCSDS Exceptions
    """
    def _init(self, *args, **kwargs):
        self.args = [a for a in args] + [a for a in kwargs.values()]

    def __repr__(self):
        return repr(self.message)

    __str__ = __repr__


class RedundantCm(MGMTException):
    """
    If the Cm number or name is already in the json file
    """
    def __init__(self, i, n, *args, **kwargs):
        self._init(i, n, *args, **kwargs)
        self.message = "Number '{}' or name '{}' of the Cm is already found "\
                       "in the json file".format(i, n)


class MissinfCm(MGMTException):
    """
    If the Cm number is not in the json file
    """
    def __init__(self, i, *args, **kwargs):
        self._init(i, *args, **kwargs)
        self.message = "Number '{}' is not found in the json file".format(i)
