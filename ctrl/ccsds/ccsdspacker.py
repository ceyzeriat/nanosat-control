#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..utils import core
from ..param import param_apid
from . import ccsdsexception
from . import param_ccsds
from . import param_category


__all__ = ['TMPacker', 'TCPacker']


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
                retdbvalues=True, **kwargs):
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
            hd['signature'] = 0
            hd['telecommand_id'] = int(tcid)
            morevalues = (('reqack_reception', 'rack', core.REQACKRECEPTION),
                          ('reqack_format', 'fack', core.REQACKFORMAT),
                          ('reqack_execution', 'eack', core.REQACKEXECUTION),
                          ('emitter_id', 'emitter', core.EMITTERID))
            # priority on short-names, then on long-names then default
            for (key, sht, defa) in morevalues:
                hd[key] = int(kwargs.pop(sht, hd.get(key, defa)))
        else:
            hd['packet_category'] = int(pktCat)
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
        maybeAux = ''
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

    def _pack_something(self, thelist, allvalues, totOctetSize, retdbvalues):
        """
        Does the packing loop for primHeader and secHeader
        """
        values = dict(allvalues)
        retvals = {}
        bits = '0' * (totOctetSize * 8)
        for item in thelist:
            if item.name not in values.keys() and item.dic_force is None:
                raise ccsdsexception.PacketValueMissing(item.name)
            retvals[item.name] = values.get(item.name, '')
            bits = core.setstr( bits,
                                item.cut,
                                item.pack(values.get(item.name, '')))
            # filling in the forced values not given as input
            if item.dic_force is not None:
                retvals[item.name] = item.dic_force
            # these are special cases that we want to fill manually because the
            # forced values are not numbers but dictionary keys
            if retdbvalues and item.non_db_dic:
                retvals[item.name] = core.bin2int(item.pack(
                                            values.get(item.name, '')))
        return bits, retvals

    def pack_primHeader(self, values, datalen, retvalues=False,
                        retdbvalues=True):
        """
        Encodes the values into a CCSDS primary header, returns hex
        string and encoded values

        Args:
        * values (dict): the values to pack
        * datalen (int): the octet-length of the data in the packet
        * retvalues (bool): if ``True``, returns the encoded values
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        # Preparation of the content of values dictionary
        values['packet_type'] = self.mode
        if self.mode == 'telecommand':
            values['data_length'] = param_ccsds.HEADER_S_SIZE_TELECOMMAND
            values['packet_category'] = '0'
            values['packet_id'] = core.get_set_next_tc_packet_id()
        else:
            values['data_length'] = param_ccsds.HEADER_S_SIZE_TELEMETRY
            values['packet_id'] = '0'
        # adds the header aux size into the packet length
        values['data_length'] += param_category.PACKETCATEGORYSIZES[
                                        int(values.get('packet_category', 0))]
        if 'pid' not in values.keys():
            raise ccsdsexception.PacketValueMissing('pid')
        values['payload_flag'] = param_apid.PLDREGISTRATION[values['pid']]
        values['level_flag'] = param_apid.LVLREGISTRATION[values['pid']]
        values['data_length'] += datalen
        bits, retvals = self._pack_something(
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
            values['days_since_ref'] = core.now2daystamp()
            values['ms_since_today'] = core.now2msstamp()
        bits, retvals = self._pack_something(thelist=hdk, allvalues=values,
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
            return ('', {}) if retvalues else ''
        pktCat = int(pktCat)
        if pktCat not in param_category.PACKETCATEGORIES.keys():
            raise ccsdsexception.CategoryMissing(pktCat)
        hdxsz = param_category.PACKETCATEGORYSIZES[pktCat]
        if hdxsz == 0:
            return ('', {}) if retvalues else ''
        bits, retvals = self._pack_something(
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
            return ('', {}) if retvalues else ''
        # encode the data here TBD
        if retvalues:
            return '', {}
        else:
            return ''

TMPacker = CCSDSPacker(mode='tm')
TCPacker = CCSDSPacker(mode='tc')
