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


from param import param_apid
from param import param_category
from .ccsdstrousseau import CCSDSTrousseau
from .ccsdskey import CCSDSKey
from ..utils import bincore
from ..utils.day import Day
from ..utils.ms import Ms


MAXIMUMDATALENGTH = 65536  # octets
MAXIMUMPACKETLENGTH = MAXIMUMDATALENGTH + 6  # octets

# length of packet as recorded in ccsds =
#   real length of packet + LENGTHMODIFIER
LENGTHMODIFIER = 0


# PRIMARY HEADER
# origin of start/end is start of packet
# start/end units is bits

def pid_pack(v, pad, **kwargs):
    pid_pack.verbose = "pid string -> binary"
    return bincore.int2bin(param_apid.PIDREGISTRATION[v], pad=pad)


def pid_unpack(v, pld, lvl, **kwargs):
    pid_unpack.verbose = "binary, payload flag and level flag -> pid string"
    dic = param_apid.PIDREGISTRATION_REV[bincore.bin2int(v)]
    return dic[int(pld)][int(lvl) if int(pld) == 0 else 1]


PACKETVERSION = CCSDSKey(   name='ccsds_version',
                            dic={0: '000'},
                            start=0,
                            l=3,
                            dic_force=0)

PACKETTYPE = CCSDSKey(  name='packet_type',
                        dic={'telemetry': '0', 'telecommand': '1'},
                        start=3,
                        l=1,
                        non_db_dic=True)

SECONDARYHEADERFLAG = CCSDSKey( name='secondary_header_flag',
                                dic={0: '0', 1: '1'},
                                start=4,
                                l=1,
                                dic_force=1)

PAYLOADFLAG = CCSDSKey( name='payload_flag',
                        dic={0: '0', 1: '1'},
                        start=5,
                        l=1)

LEVELFLAG = CCSDSKey(   name='level_flag',
                        dic={0: '0', 1: '1'},
                        start=6,
                        l=1)

PID = CCSDSKey( name='pid',
                start=7,
                l=5,
                fctunpack=pid_unpack,
                fctpack=pid_pack)

PACKETCATEGORY = CCSDSKey(  name='packet_category',
                            dic=param_category.CATEGORYREGISTRATION,
                            start=12,
                            l=4)

SEQUENCEFLAG = CCSDSKey(name='sequence_flag',
                        dic={'segment': '00', 'start': '01',
                             'end': '10', 'standalone': '11'},
                        start=16,
                        l=2,
                        dic_force='standalone',
                        non_db_dic=True)

PACKETID = CCSDSKey(name='packet_id',
                    start=18,
                    l=14,
                    fctunpack=bincore.bin2int,
                    fctpack=bincore.int2bin)

# this CCSDSKey must not be relative, i.e. there must be a "start" defined
# cf ccsdspacker.increment_data_length()
DATALENGTH = CCSDSKey(  name='data_length',
                        start=32,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)


# all keys in the right order
HEADER_P_KEYS = [PACKETVERSION, PACKETTYPE, SECONDARYHEADERFLAG, PAYLOADFLAG,
    LEVELFLAG, PID, PACKETCATEGORY, SEQUENCEFLAG, PACKETID, DATALENGTH]
HEADER_P_KEYS = CCSDSTrousseau(HEADER_P_KEYS, octets=False)


# SECONDARY HEADER TELEMETRY
# origin of start/end is end of primary header
# start/end units is bits


# length of the bit sequence useful to unambiguously determine the
# beginning of a packet
AUTHPACKETLENGTH = 12


def days_unpack(v):
    days_unpack.verbose = "binary -> unsigned integer"
    return Day(bincore.bin2int(v))


def msec_unpack(v):
    msec_unpack.verbose = "binary -> unsigned integer"
    return Ms(bincore.bin2int(v))


DAYSINCEREF_TELEMETRY = CCSDSKey(   name='days_since_ref',
                                    start=0,
                                    l=16,
                                    fctunpack=days_unpack,
                                    fctpack=bincore.int2bin)

MSECSINCEREF_TELEMETRY = CCSDSKey(  name='ms_since_today',
                                    start=16,
                                    l=32,
                                    fctunpack=msec_unpack,
                                    fctpack=bincore.int2bin)

# all keys in the right order
HEADER_S_KEYS_TELEMETRY = [DAYSINCEREF_TELEMETRY, MSECSINCEREF_TELEMETRY]
HEADER_S_KEYS_TELEMETRY = CCSDSTrousseau(HEADER_S_KEYS_TELEMETRY, octets=False)


# SECONDARY HEADER TELECOMMAND
# origin of start/end is end of primary header
# start/end units is bits

REQACKRECEPTIONTELECOMMAND = CCSDSKey(  name='reqack_reception',
                                        start=0,
                                        l=1,
                                        dic={0: '0', 1: '1'})

REQACKFORMATTELECOMMAND = CCSDSKey( name='reqack_format',
                                    start=1,
                                    l=1,
                                    dic={0: '0', 1: '1'})

REQACKEXECUTIONTELECOMMAND = CCSDSKey(  name='reqack_execution',
                                        start=2,
                                        l=1,
                                        dic={0: '0', 1: '1'})

TELECOMMANDID = CCSDSKey(   name='telecommand_id',
                            start=3,
                            l=10,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin)

EMITTERID = CCSDSKey(   name='emitter_id',
                        start=13,
                        l=3,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)

SIGNATURE = CCSDSKey(   name='signature',
                        start=16,
                        l=32,  # 128
                        fctunpack=bincore.bin2hex,
                        fctpack=bincore.hex2bin)

HEADER_S_KEYS_TELECOMMAND = [REQACKRECEPTIONTELECOMMAND,
    REQACKFORMATTELECOMMAND, REQACKEXECUTIONTELECOMMAND, TELECOMMANDID,
    EMITTERID, SIGNATURE]
HEADER_S_KEYS_TELECOMMAND = CCSDSTrousseau(HEADER_S_KEYS_TELECOMMAND,
                                            octets=False)


def disp(**hd):
    res = []
    res += ["V:{ccsds_version} T:{packet_type} SHF:{secondary_header_flag} PLD:{payload_flag} LVL:{level_flag} PID:{pid} CAT:{packet_category} SF:{sequence_flag} #:{packet_id} len:{data_length}".format(**hd)]
    res += ["Ds:{days_since_ref} Ms:{ms_since_today}".format(**hd)]
    return "\n".join(res)
