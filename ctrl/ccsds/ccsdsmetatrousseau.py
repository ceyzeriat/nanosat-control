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


from . import ccsdsexception


__all__ = ['CCSDSMetaTrousseau']


class CCSDSMetaTrousseau(object):
    def __init__(self, trousseaudict, key):
        """
        A Trousseau as a collection of CCSDS Trousseau

        Args:
          * trousseaudict (dict of Trousseau): the dictionary of
            Trousseau referred by a parameter
          * key (str): the dictionary-keyword on which trousseaudict is
            mapped
        """
        self.TROUSSEAUDIC = dict(trousseaudict)
        self.key = str(key)
        self.keys = None
        self.fmt = None
        self.size = None
        self.octets = None
        self.listof = None

    def unpack(self, data, hds, hdx):
        """
        Unpacks the data contained in the TCAnswer packet

        Args:
          * data (byts): the chain of octets to unpack
          * hds, hdx (dict): packet headers
        """
        key = int(hds.get(self.key, hdx.get(self.key)))
        if key in self.TROUSSEAUDIC:
            return self.TROUSSEAUDIC[key].unpack(data)
        else:
            raise ccsdsexception.InvalidMetaTrousseauKey(key)

    def disp(self, vals, hds, hdx):
        """
        Display the data values of the TCAnswer packet

        Args:
          * vals (dict or list of dict): a dictionary containing the
            values to display
          * hds, hdx (dict): packet headers
        """
        key = hds.get(self.key, hdx.get(self.key))
        if key in self.TROUSSEAUDIC:
            return self.TROUSSEAUDIC[key].disp(vals)
        else:
            raise ccsdsexception.InvalidMetaTrousseauKey(key)

    def pack(self, allvalues, hds, hdx, **kwargs):
        """
        Does the packing loop for the list of CCSDS keys
        Returns the bytes chain and the values encoded

        Args:
          * allvalues (dict): the values to pack
          * hds, hdx (dict): packet headers

        Kwargs:
          * passed on to the pack method of each key
        """
        key = hds.get(self.key, hdx.get(self.key))
        if key in self.TROUSSEAUDIC:
            return self.TROUSSEAUDIC[key].pack(allvalues, **kwargs)
        else:
            raise ccsdsexception.InvalidMetaTrousseauKey(key)
