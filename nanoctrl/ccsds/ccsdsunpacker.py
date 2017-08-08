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


from byt import Byt
from nanoutils import bincore
from nanoparam.categories import param_category
from nanoparam import param_ccsds


from nanoutils.ccsds import ccsdsexception as exc


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

    def unpack(self, packet):
        """
        Unpacks the packet, returns a dictionary

        Args:
        * packet (str): the string that contains the full packet
        """
        headers = self.unpack_primHeader(packet)
        headers.update(self.unpack_secHeader(packet))
        headersx = self.unpack_auxHeader(packet,
                    pldFlag=headers[param_ccsds.PAYLOADFLAG.name],
                    pktCat=headers[param_ccsds.PACKETCATEGORY.name])
        data = self.unpack_data(packet, hds=headers, hdx=headersx)
        return headers, headersx, data

    def unpack_primHeader(self, packet):
        """
        Unpacks the primary header of the packet, returns a
        dictionary

        Args:
        * packet (byts): the string that contains the full packet
        """
        header_p = {}
        chunck = packet[:param_ccsds.HEADER_P_KEYS.size]
        # prepare optionnal inputs
        header_p[param_ccsds.PAYLOADFLAG.name] = ''
        header_p[param_ccsds.LEVELFLAG.name] = ''
        for item in param_ccsds.HEADER_P_KEYS.keys:
            header_p[item.name] = item.unpack(chunck,
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
        * pldFlag (int): the payload flag of the packet
        * pktCat (int): the packet category
        """
        if self.mode == 'telecommand':
            return {}
        pldFlag = int(pldFlag)
        pktCat = int(pktCat)
        if pktCat not in param_category.CATEGORIES[pldFlag].keys():
            raise exc.CategoryMissing(pktCat, pldFlag)
        cat = param_category.CATEGORIES[pldFlag][pktCat]
        if cat.aux_size == 0:
            return {}
        start = param_ccsds.HEADER_P_KEYS.size
        if self.mode == 'telemetry':
            start += param_ccsds.HEADER_S_KEYS_TELEMETRY.size
        else:
            start += param_ccsds.HEADER_S_KEYS_TELECOMMAND.size
        return cat.aux_trousseau.unpack(packet[start:])

    def unpack_data(self, packet, hds, hdx):
        """
        Unpacks the data of the packet, returns a dictionary

        Args:
          * packet (byts): the string that contains the full packet
          * hds (dict): the packet headers
          * hdx (dict): the packet auxiliary headers
        """
        data = {'all': Byt(), 'unpacked': {}}
        start = param_ccsds.HEADER_P_KEYS.size
        if self.mode == 'telemetry':
            start += param_ccsds.HEADER_S_KEYS_TELEMETRY.size
        else:
            start += param_ccsds.HEADER_S_KEYS_TELECOMMAND.size
        catnum = int(hds[param_ccsds.PACKETCATEGORY.name])
        pld = int(hds[param_ccsds.PAYLOADFLAG.name])
        # aux header size
        cat = param_category.CATEGORIES[pld][catnum]
        start += cat.aux_size
        data['all'] = packet[start:]
        if cat.data_trousseau is not None:
            # pass tc id in case of tcanswer category
            data['unpacked'] = cat.data_trousseau.unpack(data=data['all'],
                                                         hds=hds, hdx=hdx)
        return data
