#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .ccsdskey import CCSDSKey
import .core


__all__ = [
'MAXIMUMDATALENGTH', 'MAXIMUMPACKETLENGTH', 'PACKETVERSION', 'PACKETTYPE',
'SECONDARYHEADERFLAG', 'APID', 'SEQUENCEFLAG', 'NAME', 'DATALENGTH',
'EXTENSIONFLAG', 'TIMECODEID', 'EPOCHID', 'LENGTHOFDAY', 'LENGTHOFSUBMS',
'HEADERSIZE', 'PACKETFORMAT', 'DAYSINCEREF', 'MSECSINCEREF', 'SENSORMASK']

# fonctions de conversion des HK
def tensionligne5V_fct(hx):
    return 4.59e-3 * core.hx2int(hx)

def intensiteligne_fct(hx):
    return 1.61e-3 * core.hx2int(hx)

def temp_fct(hx):
    return core.hx2int(hx) / 16.0

MAXIMUMDATALENGTH = 65536  # octets
MAXIMUMPACKETLENGTH = MAXIMUMDATALENGTH + 6  # octets

HEADERSIZE = 6  # octets
HEADERSECSIZE = 7  # octets
ACTIVESENSORS = 12

# PRIMARY HEADER
# origin of start/end is start of packet
# start/end units is bits

PACKETVERSION = CCSDSKey('PACKETVERSION', {0: '000'}, 0, 2)  # 0
PACKETTYPE = CCSDSKey('PACKETTYPE', {'telemetry': '0', 'telecommand': '1'}, 3)  # telemetry
SECONDARYHEADERFLAG = CCSDSKey('SECONDARYHEADERFLAG', {0: '0', 1: '1'}, 4)  # 1
APID = CCSDSKey('APID', {'hk_payload': '00000000011', 'science_payload': '00000000010'}, 5, 15)  # hk_payload

SEQUENCEFLAG = CCSDSKey('SEQUENCEFLAG', {'segment': '00', 'start': '01', 'end': '10', 'unsegment': '11'}, 16, 17)

NAME = CCSDSKey('NAME', {}, 18, 31, fct=core.bin2int)
DATALENGTH = CCSDSKey('DATALENGTH', {}, 32, 47, fct=core.bin2int)

# SECONDARY HEADER
# origin of start/end is end of primary header
# start/end units is bits

EXTENSIONFLAG = CCSDSKey('EXTENSIONFLAG', {0: '0', 1: '1'}, 0)  # 0
TIMECODEID = CCSDSKey('TIMECODEID', {'day': '100', 'calendar': '101'}, 1, 3)  # day

EPOCHID = CCSDSKey('EPOCHID', {'1958': '0', 'user': '1'}, 4)  # user
LENGTHOFDAY = CCSDSKey('LENGTHOFDAY', {'16': '0', '24': '1'}, 5)  # 16
LENGTHOFSUBMS = CCSDSKey('LENGTHOFSUBMS', {'none': '00', 'micro': '01', 'pico': '10'}, 6, 7)  # none

DAYSINCEREF = CCSDSKey('DAYSINCEREF', {}, 8, 23, fct=core.bin2int)
MSECSINCEREF = CCSDSKey('MSECSINCEREF', {}, 24, 56, fct=core.bin2int)

# data
# origin of start/end is end of secondary header
# start/end units is hex-chars

SENSORMASK = CCSDSKey('SENSORMASK', {}, 0, 1, fct=core.bin2int)

TENSIONLIGNE5V = CCSDSKey('TENSIONLIGNE5V', {}, 2, 3, fct=tensionligne5V_fct, unit='V')
INTENSITELIGNE5V = CCSDSKey('INTENSITELIGNE5V', {}, 4, 5, fct=intensiteligne_fct, unit='mA')
INTENSITELIGNE3V = CCSDSKey('INTENSITELIGNE3V', {}, 6, 7, fct=intensiteligne_fct, unit='mA')
TENSIONPIEZO = CCSDSKey('TENSIONPIEZO', {}, 8, 9, fct=None, unit='V')
INTENSITEPIEZO = CCSDSKey('INTENSITEPIEZO', {}, 10, 11, fct=None, unit='mA')
TENSIONVITEC = CCSDSKey('TENSIONVITEC', {}, 12, 13, fct=None, unit='mA')
TEMPDIODE = CCSDSKey('TEMPDIODE', {}, 14, 15, fct=None, unit='C')
TENSIONERRORTHERM = CCSDSKey('TENSIONERRORTHERM', {}, 16, 17, fct=None, unit='?')
TENSIONVREF = CCSDSKey('TENSIONVREF', {}, 18, 19, fct=None, unit='?')
TEMP1 = CCSDSKey('TEMP1', {}, 20, 21, fct=temp_fct, unit='C')
TEMP2 = CCSDSKey('TEMP2', {}, 22, 23, fct=temp_fct, unit='C')
TEMP3 = CCSDSKey('TEMP3', {}, 24, 25, fct=temp_fct, unit='C')


PACKETFORMAT = PACKETVERSION[0] + PACKETTYPE['telemetry'] + SECONDARYHEADERFLAG[1] + APID['hk_payload']\
               + SEQUENCEFLAG['segment'] + '{----NAME----}'\
               + '{--DATALENGTH--}'\
               + EXTENSIONFLAG[0] + TIMECODEID['day'] + EPOCHID['user'] + LENGTHOFDAY['16']\
               + LENGTHOFSUBMS['none']\
               + '{--DAYSINCEREF--}{--MSECSINCEREF--}'\
