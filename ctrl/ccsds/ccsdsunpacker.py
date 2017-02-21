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


from param import param_category
from param import param_science_hf
from ..utils import core
from . import ccsdsexception
from . import param_ccsds


__all__ = []


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
        headers.update(self.unpack_secHeader(packet, retdbvalues=retdbvalues))
        headersx = self.unpack_auxHeader(packet,
                    packetCategory=headers[param_ccsds.PACKETCATEGORY.name],
                    retdbvalues=retdbvalues)
        data = self.unpack_data(packet, hds=headers, retdbvalues=retdbvalues)
        return headers, headersx, data

    def unpack_primHeader(self, packet, retdbvalues=True):
        """
        Unpacks the primary header of the packet, returns a
        dictionary

        Args:
        * packet (str): the string that contains the full packet
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        header_p = {}
        bits = core.hex2bin(packet[:param_ccsds.HEADER_P_SIZE],
                                pad=param_ccsds.HEADER_P_SIZE * 8)
        # prepare optionnal inputs
        header_p[param_ccsds.PAYLOADFLAG.name] = ''
        header_p[param_ccsds.LEVELFLAG.name] = ''
        for item in param_ccsds.HEADER_P_KEYS:
            if retdbvalues and item.non_db_dic:
                header_p[item.name] = core.bin2int(item.unpack(bits, raw=True))
            else:
                header_p[item.name] = item.unpack(bits,
                                pld=header_p[param_ccsds.PAYLOADFLAG.name],
                                lvl=header_p[param_ccsds.LEVELFLAG.name])
        return header_p

    def unpack_secHeader(self, packet, retdbvalues=True):
        """
        Unpacks the secodnary header of the packet, returns a
        dictionary

        Args:
        * packet (str): the string that contains the full packet
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        header_s = {}
        if self.mode == 'telemetry':
            hskey = param_ccsds.HEADER_S_KEYS_TELEMETRY
            hssz = param_ccsds.HEADER_S_SIZE_TELEMETRY
        else:
            hskey = param_ccsds.HEADER_S_KEYS_TELECOMMAND
            hssz = param_ccsds.HEADER_S_SIZE_TELECOMMAND
        start = param_ccsds.HEADER_P_SIZE
        bits = core.hex2bin(packet[start:start+hssz], pad=hssz*8)
        for item in hskey:
            header_s[item.name] = item.unpack(bits)
        return header_s

    def unpack_auxHeader(self, packet, packetCategory, retdbvalues=True):
        """
        Unpacks the auxiliary header of the packet, returns a
        dictionary

        Args:
        * packet (str): the string that contains the full packet
        * packetCategory (int): the packet category
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        header_x = {}
        if self.mode == 'telecommand':
            return header_x
        if packetCategory not in param_category.PACKETCATEGORIES.keys():
            raise ccsdsexception.CategoryMissing(packetCategory)
        hxsz = param_category.PACKETCATEGORYSIZES[packetCategory]
        if hxsz == 0:
            return header_x
        hpssz = param_ccsds.HEADER_P_SIZE
        if self.mode == 'telemetry':
            hpssz += param_ccsds.HEADER_S_SIZE_TELEMETRY
        else:
            hpssz += param_ccsds.HEADER_S_SIZE_TELECOMMAND
        bits = core.hex2bin(packet[hpssz:hpssz+hxsz], pad=hxsz*8)
        for item in param_category.PACKETCATEGORIES[packetCategory]:
            header_x[item.name] = item.unpack(bits)
        return header_x

    def unpack_data(self, packet, hds, retdbvalues=True):
        """
        Unpacks the data of the packet, returns a dictionary

        Args:
        * packet (str): the string that contains the full packet
        * hds (int): the packet header
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        data = {}
        hsz = param_ccsds.HEADER_P_SIZE
        if self.mode == 'telemetry':
            hsz += param_ccsds.HEADER_S_SIZE_TELEMETRY
        else:
            hsz += param_ccsds.HEADER_S_SIZE_TELECOMMAND
        hsz += param_category.PACKETCATEGORYSIZES[
                            hds[param_ccsds.PACKETCATEGORY.name]]
        data['all'] = packet[hsz:]
        if param_category.TABLEDATACRUNCHING is None:
            return data  # no specifics unpacking data
        params = getattr(param, param_category.TABLEDATACRUNCHING[
                                    hds[param_ccsds.PACKETCATEGORY.name]])
        data['unpacked'] = params.unpack(data['all'])
        return data
