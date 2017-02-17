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
from param import param_apid
from ..utils import core
from ..utils import Byt
from . import ccsdsexception
from . import param_ccsds


__all__ = []


class CCSDSPacker(object):
    def __init__(self, mode='tc'):
        """
        A CCSDS packer

        Args:
        * mode (str): 'tm' or 'tc' for telemetry or telecommand
        """
        self.mode = 'telemetry' if str(mode).lower()[1] == 'm'\
                        else 'telecommand'

    def pack(self, pid, data='', tcid='', pktCat=0, retvalues=True,
                retdbvalues=True, withPacketID=True, **kwargs):
        """
        Creates a packet, returns the packet string and optionally
        the dictionnaries of primary/secondary and auxiliary headers

        Args:
        * pid (str): the process id related to the packet
        * data (str): only for TC-mode, the data to include in the
          packet
        * tcid (int): only for TC-mode, the id of the telecommand
        * pktCat (int): only for TM-mode, the packet category
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        * withPacketID (bool): set to ``False`` to deactivate the
          packet id determination

        Kwargs for TC-mode:
        * rack (bool) [default: {}]: ``True`` to recieve the
          acknowledgement of reception
        * fack (bool) [default: {}]: ``True`` to recieve the
          acknowledgement of format
        * eack (bool) [default: {}]: ``True`` to recieve the
          acknowledgement of execution
        * emitter (int) [default: {}]: the id of the emitter

        Kwargs for TM-mode:
        * auxiliary header and data keys-values
        """.format(core.REQACKRECEPTION, core.REQACKFORMAT,
                    core.REQACKEXECUTION, core.EMITTERID)
        tm = (self.mode == 'telemetry')
        hd = {}
        hd['pid'] = pid
        if not tm:
            hd['signature'] = Byt("\x00"*(param_ccsds.SIGNATURE.len//8))
            hd['telecommand_id'] = int(tcid)
            morevalues = ((param_ccsds.REQACKRECEPTIONTELECOMMAND.name, 'rack',
                            core.REQACKRECEPTION),
                          (param_ccsds.REQACKFORMATTELECOMMAND.name, 'fack',
                            core.REQACKFORMAT),
                          (param_ccsds.REQACKEXECUTIONTELECOMMAND.name, 'eack',
                            core.REQACKEXECUTION),
                          (param_ccsds.EMITTERID.name, 'emitter',
                            core.EMITTERID))
            # priority on short-names, then on long-names then default
            for (key, sht, defa) in morevalues:
                hd[key] = int(kwargs.pop(sht, hd.get(key, defa)))
        else:
            hd[param_ccsds.PACKETCATEGORY.name] = int(pktCat)
        # header prim
        retprim = self.pack_primHeader(values=hd, datalen=len(data),
                                        retvalues=True,
                                        retdbvalues=retdbvalues)
        # header sec
        retsec = self.pack_secHeader(values=hd, retvalues=True,
                                        retdbvalues=retdbvalues)
        # make header
        hds = {}
        hds.update(retprim[1])
        hds.update(retsec[1])
        maybeAux = Byt()
        hdx = {}
        retd = {}
        # header aux
        retaux = self.pack_auxHeader(values=kwargs, pktCat=pktCat,
                                        retvalues=True,
                                        retdbvalues=retdbvalues)
        maybeAux = retaux[0]
        hdx.update(retaux[1])
        # only if telemetry
        if tm:
            # data
            retdata = self.pack_data(values=kwargs, header=hds,
                                        retvalues=True,
                                        retdbvalues=retdbvalues)
            data = retdata[0]
            retd.update(retdata[1])
        if retvalues:
            return retprim[0] + retsec[0] + maybeAux + data, hds, hdx, retd
        else:
            return retprim[0] + retsec[0] + maybeAux + data

    def pack_primHeader(self, values, datalen, retvalues=False,
                        retdbvalues=True, withPacketID=True):
        """
        Encodes the values into a CCSDS primary header, returns hex
        string and encoded values

        Args:
        * values (dict): the values to pack
        * datalen (int): the octet-length of the data in the packet
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        * withPacketID (bool): set to ``False`` to deactivate the
          packet id determination
        """
        # Preparation of the content of values dictionary
        values[param_ccsds.PACKETTYPE.name] = self.mode
        if self.mode == 'telecommand':
            values[param_ccsds.DATALENGTH.name] =\
                param_ccsds.HEADER_S_SIZE_TELECOMMAND
            values[param_ccsds.PACKETCATEGORY.name] = '0'
            if withPacketID:
                values[param_ccsds.PACKETID.name] =\
                    core.get_set_next_tc_packet_id()
            else:
                values[param_ccsds.PACKETID.name] = '0'
        else:
            values[param_ccsds.DATALENGTH.name] =\
                param_ccsds.HEADER_S_SIZE_TELEMETRY
            values[param_ccsds.PACKETID.name] = '0'
        # adds the header aux size into the packet length
        values[param_ccsds.DATALENGTH.name] +=\
            param_category.PACKETCATEGORYSIZES[\
                int(values.get(param_ccsds.PACKETCATEGORY.name, 0))]
                                        
        if param_ccsds.PID.name not in values.keys():
            raise ccsdsexception.PacketValueMissing(param_ccsds.PID.name)
        values[param_ccsds.PAYLOADFLAG.name] =\
            param_apid.PLDREGISTRATION[values[param_ccsds.PID.name]]
        values[param_ccsds.LEVELFLAG.name] =\
            param_apid.LVLREGISTRATION[values[param_ccsds.PID.name]]
        values[param_ccsds.DATALENGTH.name] += datalen
        bits, retvals = _pack_something(
                                thelist=param_ccsds.HEADER_P_KEYS,
                                allvalues=values,
                                totOctetSize=param_ccsds.HEADER_P_SIZE,
                                retdbvalues=retdbvalues)
        if retvalues:
            return core.bin2hex(bits, pad=param_ccsds.HEADER_P_SIZE), retvals
        else:
            return core.bin2hex(bits, pad=param_ccsds.HEADER_P_SIZE)

    def pack_secHeader(self, values, retvalues=False, retdbvalues=True):
        """
        Encodes the values into a CCSDS secondary header, returns hex
        string and encoded values

        Args:
        * values (dict): the values to pack
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        if self.mode == 'telecommand':
            hdk = param_ccsds.HEADER_S_KEYS_TELECOMMAND
            hdsz = param_ccsds.HEADER_S_SIZE_TELECOMMAND
        else:
            hdk = param_ccsds.HEADER_S_KEYS_TELEMETRY
            hdsz = param_ccsds.HEADER_S_SIZE_TELEMETRY
            values[param_ccsds.DAYSINCEREF_TELEMETRY.name] = core.now2daystamp()
            values[param_ccsds.MSECSINCEREF_TELEMETRY.name] = core.now2msstamp()
        bits, retvals = _pack_something(thelist=hdk, allvalues=values,
                                totOctetSize=hdsz, retdbvalues=retdbvalues)
        if retvalues:
            return core.bin2hex(bits, pad=hdsz), retvals
        else:
            return core.bin2hex(bits, pad=hdsz)

    def pack_auxHeader(self, values, pktCat, retvalues=False, retdbvalues=True):
        """
        Encodes the values into a CCSDS auxiliary header, returns hex
        string and encoded values

        Args:
        * values (dict): the values to pack
        * pktCat (int): only for TM-mode, the packet category
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        if self.mode != 'telemetry':
            return (Byt(), {}) if retvalues else Byt()
        pktCat = int(pktCat)
        if pktCat not in param_category.PACKETCATEGORIES.keys():
            raise ccsdsexception.CategoryMissing(pktCat)
        hdxsz = param_category.PACKETCATEGORYSIZES[pktCat]
        if hdxsz == 0:
            return (Byt(), {}) if retvalues else Byt()
        bits, retvals = _pack_something(
                            thelist=param_category.PACKETCATEGORIES[pktCat],
                            allvalues=values,
                            totOctetSize=hdxsz,
                            retdbvalues=retdbvalues)
        if retvalues:
            return core.bin2hex(bits, pad=hdxsz), retvals
        else:
            return core.bin2hex(bits, pad=hdxsz)

    def pack_data(self, values, header, retvalues=False, retdbvalues=True):
        """
        Encodes the values into a CCSDS auxiliary header, returns hex
        string and encoded values

        Args:
        * values (dict): the values to pack
        * header (dict): 
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        if self.mode != 'telemetry':
            return (Byt(), {}) if retvalues else Byt()
        # encode the data here TBD
        if retvalues:
            return Byt(), {}
        else:
            return Byt()

def _pack_something(thelist, allvalues, totOctetSize, retdbvalues):
    """
    Does the packing loop for a list of CCSDS keys
    """
    values = dict(allvalues)
    retvals = {}
    bits = '0' * (totOctetSize * 8)
    for item in thelist:
        if item.name not in values.keys() and item.dic_force is None:
            raise ccsdsexception.PacketValueMissing(item.name)
        retvals[item.name] = values.get(item.name, '')
        bits = setstr( bits,
                            item.cut,
                            item.pack(values.get(item.name, '')))
        # filling in the forced values not given as input
        if item.dic_force is not None:
            retvals[item.name] = item.dic_force
        # these are special cases that we want to fill manually because the
        # forced values are not numbers but dictionary keys
        if retdbvalues and item.non_db_dic:
            retvals[item.name] = bin2int(item.pack(
                                                values.get(item.name, '')))
    return bits, retvals
