#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .ccsdskey import CCSDSKey
from .. import core
from .. import param_apid
from .. import param_category


MAXIMUMDATALENGTH = 65536  # octets
MAXIMUMPACKETLENGTH = MAXIMUMDATALENGTH + 6  # octets



# PRIMARY HEADER
# origin of start/end is start of packet
# start/end units is bits

def get_pid(v, pad, **kwargs):
    return core.int2bin(param_apid.APIDREGISTRATION[v], pad=pad)

def get_pid_rev(v, pld, lvl, **kwargs):
    dic = param_apid.APIDREGISTRATION_REV
    return dic[int(pld)][int(lvl) if int(pld) == 0 else 1]

HEADER_P_SIZE = 6  # octets

PACKETVERSION = CCSDSKey(   name='packet_version',
                            dic={0: '000'},
                            start=0,
                            l=3,
                            dic_force=0)

PACKETTYPE = CCSDSKey(  name='packet_type',
                        dic={'telemetry': '0', 'telecommand': '1'},
                        start=3,
                        l=1)

SECONDARYHEADERFLAG = CCSDSKey( name='secondary_header_flag',
                                dic={0: '0', 1: '1'},
                                start=4,
                                l=1,
                                dic_force=1)

PAYLOADFLAG = CCSDSKey( name='payload_flag',
                        dic={0: '0', 1: '1'},
                        start=5, l=1)

LEVELFLAG = CCSDSKey(   name='level_flag',
                        dic={0: '0', 1: '1'},
                        start=6,
                        l=1)

PID = CCSDSKey( name='pid',
                start=7,
                l=5,
                fctdepack=get_pid_rev,
                fctpack=get_pid)

PACKETCATEGORY = CCSDSKey(  name='packet_category',
                            dic=param_category.CATEGORYREGISTRATION,
                            start=12,
                            l=4)

SEQUENCEFLAG = CCSDSKey(name='sequence_flag',
                        dic={'segment': '00', 'start': '01', 'end': '10', 'standalone': '11'},
                        start=16,
                        l=2,
                        dic_force='standalone')

PACKETID = CCSDSKey(name='packet_id',
                    start=18,
                    l=14,
                    fctdepack=core.bin2int,
                    fctpack=core.int2bin)

DATALENGTH = CCSDSKey(  name='data_length',
                        start=32,
                        l=16,
                        fctdepack=core.bin2int,
                        fctpack=core.int2bin)


# all keys in the right order
HEADER_P_KEYS = [PACKETVERSION, PACKETTYPE, SECONDARYHEADERFLAG, PID, PAYLOADFLAG, LEVELFLAG, PACKETCATEGORY, SEQUENCEFLAG, PACKETID, DATALENGTH]



# SECONDARY HEADER TELEMETRY
# origin of start/end is end of primary header
# start/end units is bits

HEADER_S_SIZE_TELEMETRY = 6  # octets

DAYSINCEREF_TELEMETRY = CCSDSKey(   name='days_since_ref',
                                    start=0,
                                    l=16,
                                    fctdepack=core.bin2int,
                                    fctpack=core.int2bin)

MSECSINCEREF_TELEMETRY = CCSDSKey(  name='ms_since_ref',
                                    start=16,
                                    l=32,
                                    fctdepack=core.bin2int,
                                    fctpack=core.int2bin)

# all keys in the right order
HEADER_S_KEYS_TELEMETRY = [DAYSINCEREF_TELEMETRY, MSECSINCEREF_TELEMETRY]



# SECONDARY HEADER TELECOMMAND
# origin of start/end is end of primary header
# start/end units is bits

HEADER_S_SIZE_TELECOMMAND = 6  # octets

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
                            fctdepack=core.bin2int,
                            fctpack=core.int2bin)

EMITTERID = CCSDSKey(   name='emitter_id',
                        start=13,
                        l=3,
                        fctdepack=core.bin2int,
                        fctpack=core.int2bin)

SIGNATURE = CCSDSKey(   name='signature',
                        start=16,
                        l=32,
                        fctdepack=core.bin2int,
                        fctpack=core.int2bin)

HEADER_S_KEYS_TELECOMMAND = [REQACKRECEPTIONTELECOMMAND, REQACKFORMATTELECOMMAND, REQACKEXECUTIONTELECOMMAND, TELECOMMANDID, EMITTERID, SIGNATURE]
