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


import param
from byt import Byt
from param import param_category
from ..utils import bincore
from . import ccsdsexception
from . import param_ccsds


__all__ = ['CCSDSUnPacker']


class CCSDSUnPacker(object):
    def __init__(self, mode='tm'):
        """
        A CCSDS unpacker

        Args:
        * mode (str): 'tm' or 'tc' for telemetry or telecommand
        """
        self.mode = 'telecommand' if str(mode).lower()[1] == 'c'\
                        else 'telemetry'

    def unpack(self, packet, retdbvalues=True):
        """
        Unpacks the packet, returns a dictionary

        Args:
        * packet (str): the string that contains the full packet
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        headers = {}
        headers.update(self.unpack_primHeader(packet, retdbvalues=retdbvalues))
        headers.update(self.unpack_secHeader(packet))
        headersx = self.unpack_auxHeader(packet,
                    pldFlag=headers[param_ccsds.PAYLOADFLAG.name],
                    pktCat=headers[param_ccsds.PACKETCATEGORY.name])
        data = self.unpack_data(packet, hds=headers)
        return headers, headersx, data

    def unpack_primHeader(self, packet, retdbvalues=True):
        """
        Unpacks the primary header of the packet, returns a
        dictionary

        Args:
        * packet (byts): the string that contains the full packet
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        header_p = {}
        bits = bincore.hex2bin(packet[:param_ccsds.HEADER_P_KEYS.size])
        # prepare optionnal inputs
        header_p[param_ccsds.PAYLOADFLAG.name] = ''
        header_p[param_ccsds.LEVELFLAG.name] = ''
        for item in param_ccsds.HEADER_P_KEYS.keys:
            if retdbvalues and item.non_db_dic:
                header_p[item.name] = bincore.bin2int(item.unpack(bits,
                                                                  raw=True))
            else:
                header_p[item.name] = item.unpack(bits,
                                pld=header_p[param_ccsds.PAYLOADFLAG.name],
                                lvl=header_p[param_ccsds.LEVELFLAG.name])
        return header_p

    def unpack_secHeader(self, packet):
        """
        Unpacks the secodnary header of the packet, returns a
        dictionary

        Args:
        * packet (byts): the string that contains the full packet
        """
        if self.mode == 'telemetry':
            hskey = param_ccsds.HEADER_S_KEYS_TELEMETRY
        else:
            hskey = param_ccsds.HEADER_S_KEYS_TELECOMMAND
        return hskey.unpack(packet[param_ccsds.HEADER_P_KEYS.size:])

    def unpack_auxHeader(self, packet, pldFlag, pktCat):
        """
        Unpacks the auxiliary header of the packet, returns a
        dictionary

        Args:
        * packet (byts): the string that contains the full packet
        * pldFlag (bool): the payload flag of the packet
        * pktCat (int): the packet category
        """
        if self.mode == 'telecommand':
            return {}
        if pktCat not in param_category.PACKETCATEGORIES[int(pldFlag)].keys():
            raise ccsdsexception.CategoryMissing(pktCat, pldFlag)
        hx = param_category.PACKETCATEGORIES[int(pldFlag)][pktCat]
        if hx.size == 0:
            return {}
        start = param_ccsds.HEADER_P_KEYS.size
        if self.mode == 'telemetry':
            start += param_ccsds.HEADER_S_KEYS_TELEMETRY.size
        else:
            start += param_ccsds.HEADER_S_KEYS_TELECOMMAND.size
        return hx.unpack(packet[start:])

    def unpack_data(self, packet, hds):
        """
        Unpacks the data of the packet, returns a dictionary

        Args:
        * packet (byts): the string that contains the full packet
        * hds (int): the packet headers
        """
        data = {'all': Byt(), 'unpacked': {}}
        start = param_ccsds.HEADER_P_KEYS.size
        if self.mode == 'telemetry':
            start += param_ccsds.HEADER_S_KEYS_TELEMETRY.size
        else:
            start += param_ccsds.HEADER_S_KEYS_TELECOMMAND.size
        cat = int(hds[param_ccsds.PACKETCATEGORY.name])
        pld = int(hds[param_ccsds.PAYLOADFLAG.name])
        # aux header size
        start += param_category.PACKETCATEGORYSIZES[pld][cat]
        data['all'] = packet[start:]
        cat_params = param_category.FILEDATACRUNCHING[pld][cat]
        if cat_params is None:
            return data  # no specifics for unpacking data
        else:
            TROUSSEAU = getattr(param, cat_params).TROUSSEAU
        data['unpacked'] = TROUSSEAU.unpack(data['all'])
        return data
