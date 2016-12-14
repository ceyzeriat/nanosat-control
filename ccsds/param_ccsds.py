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

HEADER_P_SIZE = 6  # octets

PACKETVERSION = CCSDSKey('packet_version', dic={0: '000'}, start=0, l=3)  # 0
PACKETVERSION_VALUE = 0

PACKETTYPE = CCSDSKey('packet_type', dic={'telemetry': '0', 'telecommand': '1'}, start=3, l=1)

SECONDARYHEADERFLAG = CCSDSKey('secondary_header_flag', dic={0: '0', 1: '1'}, start=4, l=1)  # 1

PAYLOADFLAG = CCSDSKey('payload_flag', dic={0: '0', 1: '1'}, start=5, l=1)

LEVELFLAG = CCSDSKey('level_flag', dic={0: '0', 1: '1'}, start=6, l=1)

PID = CCSDSKey('apid', dic=param_apid.APIDREGISTRATION, start=7, l=5)

PACKETCATEGORY = CCSDSKey('packet_category', dic=param_category.CATEGORYREGISTRATION, start=12, l=4)

SEQUENCEFLAG = CCSDSKey('sequence_flag', dic={'segment': '00', 'start': '01', 'end': '10', 'standalone': '11'}, start=16, l=2)
SEQUENCEFLAG_VALUE = 'standalone'

PACKETID = CCSDSKey('packet_id', start=18, l=14, fct=core.bin2int, fctrev=core.int2bin)

DATALENGTH = CCSDSKey('data_length', start=32, l=16, fct=core.bin2int, fctrev=core.int2bin)


# all keys in the right order
HEADER_P_KEYS = [PACKETVERSION, PACKETTYPE, SECONDARYHEADERFLAG, PAYLOADFLAG, LEVELFLAG, PID, PACKETCATEGORY, SEQUENCEFLAG, PACKETID, DATALENGTH]



# SECONDARY HEADER TELEMETRY
# origin of start/end is end of primary header
# start/end units is bits

HEADER_S_SIZE_TELEMETRY = 6  # octets

DAYSINCEREF_TELEMETRY = CCSDSKey('days_since_ref', start=0, l=16, fct=core.bin2int)

MSECSINCEREF_TELEMETRY = CCSDSKey('ms_since_ref', start=16, l=32, fct=core.bin2int)

# all keys in the right order
HEADER_S_KEYS_TELEMETRY = [DAYSINCEREF_TELEMETRY, MSECSINCEREF_TELEMETRY]



# SECONDARY HEADER TELECOMMAND
# origin of start/end is end of primary header
# start/end units is bits

HEADER_S_SIZE_TELECOMMAND = 6  # octets

REQACKRECEPTIONTELECOMMAND = CCSDSKey('reqack_reception', start=0, l=1, dic={0: '0', 1: '1'})

REQACKFORMATTELECOMMAND = CCSDSKey('reqack_format', start=1, l=1, dic={0: '0', 1: '1'})

REQACKEXECUTIONTELECOMMAND = CCSDSKey('reqack_execution', start=2, l=1, dic={0: '0', 1: '1'})

TELECOMMANDID = CCSDSKey('telecommand_id', start=3, l=10, fct=core.bin2int)

EMITTERID = CCSDSKey('emitter_id', start=13, l=3, fct=core.bin2int)

SIGNATURE = CCSDSKey('signature', start=16, l=32, fct=core.bin2int)

HEADER_S_KEYS_TELEMETRY = [REQACKRECEPTIONTELECOMMAND, REQACKFORMATTELECOMMAND, REQACKEXECUTIONTELECOMMAND, TELECOMMANDID, EMITTERID, SIGNATURE]
