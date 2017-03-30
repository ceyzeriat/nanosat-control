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
from param import param_category
from param import param_apid
from param import param_all
from ..utils import core
from ..utils import hmac
from ..utils import bincore
from . import ccsdsexception
from . import param_ccsds


__all__ = ['CCSDSPacker']


class CCSDSPacker(object):
    def __init__(self, mode='tc'):
        """
        A CCSDS packer

        Args:
          * mode (str): 'tm' or 'tc' for telemetry or telecommand
        """
        self.mode = 'telemetry' if str(mode).lower()[1] == 'm'\
                        else 'telecommand'

    def pack(self, pid, TCdata='', TCid='', pktCat=None, retvalues=True,
                retdbvalues=True, withPacketID=True, **kwargs):
        """
        Creates a packet, returns the packet string and optionally
        the dictionnaries of primary/secondary and auxiliary headers

        Args:
          * pid (str): the process string-id related to the packet
          * TCdata (byts): only for TC-mode, the data to include in the
            packet
          * TCid (int): only for TC-mode, the id of the telecommand
          * pktCat (int): only for TM-mode, the packet category
          * retvalues (bool): if ``True``, returns the encoded values
          * retdbvalues (bool): if ``True``, returns the encoded values
            in a format directly compatible with the database
          * withPacketID (bool): set to ``False`` to deactivate the
            packet id determination

        Kwargs for TC-mode:
          * rack (bool) [default: REQACKRECEPTION]: ``True`` to recieve the
            acknowledgement of reception
          * fack (bool) [default: REQACKFORMAT]: ``True`` to recieve the
            acknowledgement of format
          * eack (bool) [default: REQACKEXECUTION]: ``True`` to recieve the
            acknowledgement of execution
          * emitter (int) [default: EMITTERID]: the id of the emitter
          * signit (bool) [default: USESIGGY]: sign the packet or not

        Kwargs for TM-mode:
          * auxiliary header and data keys-values
        """
        hd = {}
        hd[param_ccsds.PID.name] = str(pid).lower()
        if not self.mode == 'telemetry':
            hd[param_ccsds.SIGNATURE.name] =\
                Byt("\x00"*(param_ccsds.SIGNATURE.len//8))
            hd[param_ccsds.TELECOMMANDID.name] = int(TCid)
            morevalues = ((param_ccsds.REQACKRECEPTIONTELECOMMAND.name, 'rack',
                            param_all.REQACKRECEPTION),
                          (param_ccsds.REQACKFORMATTELECOMMAND.name, 'fack',
                            param_all.REQACKFORMAT),
                          (param_ccsds.REQACKEXECUTIONTELECOMMAND.name, 'eack',
                            param_all.REQACKEXECUTION),
                          (param_ccsds.EMITTERID.name, 'emitter',
                            param_all.EMITTERID))
            # priority on short-names, then on long-names then default
            for (key, sht, defa) in morevalues:
                hd[key] = int(kwargs.pop(sht, hd.get(key, defa)))
        else:
            hd[param_ccsds.PACKETCATEGORY.name] = int(pktCat)
        # header prim
        retprim = self.pack_primHeader(values=hd, datalen=len(TCdata),
                                        retvalues=True,
                                        retdbvalues=retdbvalues)
        # header sec
        retsec = self.pack_secHeader(values=hd, retvalues=True,
                                        retdbvalues=retdbvalues)
        # make header return values
        hds = {}
        hds.update(retprim[1])
        hds.update(retsec[1])
        maybeAux = Byt()
        hdx = {}
        retd = {}
        # header aux
        retaux = self.pack_auxHeader(values=kwargs,
                            pldFlag=hds[param_ccsds.PAYLOADFLAG.name],
                            pktCat=pktCat, retvalues=True,
                            retdbvalues=retdbvalues)
        maybeAux = retaux[0]
        hdx.update(retaux[1])
        # only if telemetry
        if self.mode == 'telemetry':
            # data
            retdata = self.pack_data(values=kwargs, header=hds,
                                        retvalues=True,
                                        retdbvalues=retdbvalues)
            data = retdata[0]
            retd.update(retdata[1])
            retprim = self.increment_data_length(
                                    datalen=len(data),
                                    primaryHDpacket=retprim[0],
                                    primaryHDdict=(retprim[1:]+(None,))[1])
        else:
            data = TCdata
        theFullPacket = retprim[0] + retsec[0] + maybeAux + data
        if kwargs.pop('signit', param_all.USESIGGY)\
                                and self.mode != 'telemetry':
            theFullPacket = self.add_siggy(theFullPacket)
        if retvalues:
            return theFullPacket, hds, hdx, retd
        else:
            return theFullPacket

    def add_siggy(self, fullPacket):
        # calculates the signature from full packet
        siggy = hmac(fullPacket)
        # apply mask
        siggy = Byt([s for idx, s in enumerate(siggy.ints())\
                        if core.KEYMASK[idx] == '1'])
        # fuck indians
        if bincore.TWINKLETWINKLELITTLEINDIA:
            siggy = siggy[::-1]
        # grab the bounds of the siggy location, to chunk it into the packet
        startSiggy = param_ccsds.HEADER_P_KEYS.size +\
                                param_ccsds.SIGNATURE.start//8
        # return concatenated turd
        return fullPacket[:startSiggy] + siggy +\
                fullPacket[startSiggy + param_ccsds.SIGNATURE.len//8:]

    def pack_primHeader(self, values, datalen=0, retvalues=False,
                        retdbvalues=True, withPacketID=True):
        """
        Encodes the values into a CCSDS primary header, returns hex
        string and encoded values

        Args:
          * values (dict): the values to pack, with pid as pid string-id
          * datalen (int): the length of the data. If not known yet, it
            can be be 'manually' updated using ``increment_data_length``
            method
          * retvalues (bool): if ``True``, returns the encoded values
          * retdbvalues (bool): if ``True``, returns the encoded values
            in a format directly compatible with the database
          * withPacketID (bool): set to ``False`` to deactivate the
            packet id determination
        """
        # Preparation of the content of values dictionary
        values[param_ccsds.PACKETTYPE.name] = self.mode
        # CCSDS length has a modifier versus real packet length
        values[param_ccsds.DATALENGTH.name] = param_ccsds.LENGTHMODIFIER
        if self.mode == 'telecommand':
            values[param_ccsds.DATALENGTH.name] +=\
                param_ccsds.HEADER_S_KEYS_TELECOMMAND.size
            # force packet category to 0
            values[param_ccsds.PACKETCATEGORY.name] = '0'
            # want to increment packet id?
            if withPacketID:
                values[param_ccsds.PACKETID.name] =\
                    core.get_set_next_tc_packet_id()
            else:
                values[param_ccsds.PACKETID.name] = '0'
        else:
            values[param_ccsds.DATALENGTH.name] +=\
                param_ccsds.HEADER_S_KEYS_TELEMETRY.size
            # don't bother about packet id, not supported
            values[param_ccsds.PACKETID.name] = '0'
        # check pid string
        if param_ccsds.PID.name not in values.keys():
            raise ccsdsexception.PacketValueMissing(param_ccsds.PID.name)
        pidstr = values[param_ccsds.PID.name]
        if pidstr not in param_apid.PIDREGISTRATION.keys():
            raise ccsdsexception.PIDMissing(pidstr)
        values[param_ccsds.PID.name] =\
            param_apid.PIDREGISTRATION[pidstr]
        # fill in payload and level flags from pid string
        values[param_ccsds.PAYLOADFLAG.name] =\
            param_apid.PLDREGISTRATION[pidstr]
        values[param_ccsds.LEVELFLAG.name] =\
            param_apid.LVLREGISTRATION[pidstr]
        # add the header aux size into the packet length
        if not self.mode == 'telecommand':
            values[param_ccsds.DATALENGTH.name] +=\
                param_category.PACKETCATEGORYSIZES[\
                    int(values[param_ccsds.PAYLOADFLAG.name])][\
                    int(values.get(param_ccsds.PACKETCATEGORY.name, 0))]
        # update the length with data length
        values[param_ccsds.DATALENGTH.name] += int(datalen)
        data, retvals = param_ccsds.HEADER_P_KEYS.pack(allvalues=values,
                                                    retdbvalues=retdbvalues)
        if retvalues:
            return data, retvals
        else:
            return data

    def increment_data_length(self, datalen, primaryHDpacket,
                                primaryHDdict=None):
        """
        Updates the primary header with the real data length
        NB: this method increments the packet information with the value
        of ``datalen``, meaning that it does know nor care

        Args:
          * datalen (int): the length of the data
          * primaryHDpacket (Byt): the primary header as octets
          * primaryHDdict (dict): the primary packet as dictionary.
            If not provided, (default is ``None``), ``None`` will
            be returned instead of the dictionary
        """
        lenkey = param_ccsds.DATALENGTH
        bits = bincore.hex2bin(primaryHDpacket)
        ll = lenkey.unpack(bits) + datalen
        bits = core.setstr(bits, lenkey.cut, lenkey.pack(ll))
        primaryHDpacket = bincore.bin2hex(bits, pad=len(primaryHDpacket))
        if primaryHDdict is not None:
            primaryHDdict[param_ccsds.DATALENGTH.name] += datalen
        return primaryHDpacket, primaryHDdict

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
        else:
            hdk = param_ccsds.HEADER_S_KEYS_TELEMETRY
            values[param_ccsds.DAYSINCEREF_TELEMETRY.name] = core.now2daystamp()
            values[param_ccsds.MSECSINCEREF_TELEMETRY.name] = core.now2msstamp()
        data, retvals = hdk.pack(allvalues=values, retdbvalues=retdbvalues)
        if retvalues:
            return data, retvals
        else:
            return data

    def pack_auxHeader(self, values, pldFlag, pktCat, retvalues=False, retdbvalues=True):
        """
        Encodes the values into a CCSDS auxiliary header, returns hex
        string and encoded values

        Args:
          * values (dict): the values to pack
          * pldFlag (bool): the payload flag of the packet
          * pktCat (int): only for TM-mode, the packet category
          * retvalues (bool): if ``True``, returns the encoded values
          * retdbvalues (bool): if ``True``, returns the encoded values
            in a format directly compatible with the database
        """
        if self.mode != 'telemetry':
            return (Byt(), {}) if retvalues else Byt()
        pktCat = int(pktCat)
        if pktCat not in param_category.PACKETCATEGORIES[int(pldFlag)].keys():
            raise ccsdsexception.CategoryMissing(pktCat, pldFlag)
        hdx = param_category.PACKETCATEGORIES[int(pldFlag)][pktCat]
        if hdx.size == 0:
            return (Byt(), {}) if retvalues else Byt()
        data, retvals = hdx.pack(allvalues=values, retdbvalues=retdbvalues)
        if retvalues:
            return data, retvals
        else:
            return data

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
