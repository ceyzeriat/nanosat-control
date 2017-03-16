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


from .ccsdstrousseau import CCSDSTrousseau
from .ccsdskey import CCSDSKey
from ..utils import bincore
from ..utils.day import Day
from ..utils.ms import Ms


MAXIMUMDATALENGTH = 65536  # octets
MAXIMUMPACKETLENGTH = MAXIMUMDATALENGTH + 6  # octets

# length of packet as recorded in ccsds - LENGTHMODIFIER =
#   real length of Packet - length of Primary Header
# the official CCSDS standard specifies that LENGTHMODIFIER = 1
LENGTHMODIFIER = 0


# PRIMARY HEADER
# origin of start/end is start of packet
# start/end units is bits


PACKETVERSION = CCSDSKey(       name='ccsds_version',
                                dic={0: '000'},
                                start=0,
                                l=3,
                                dic_force=0,
                                verbose="The CCSDS format version. Shall be 0b000",
                                disp="v")

PACKETTYPE = CCSDSKey(          name='packet_type',
                                dic={'telemetry': '0', 'telecommand': '1'},
                                start=3,
                                l=1,
                                non_db_dic=True,
                                verbose="Whether telecommand packet or telemetry packet. Shall be 0b0 for telemetry or 0b1 for telecommand",
                                disp="tc")

SECONDARYHEADERFLAG = CCSDSKey( name='secondary_header_flag',
                                dic={0: '0', 1: '1'},
                                start=4,
                                l=1,
                                dic_force=1,
                                verbose="Is there a secondary header? Always true, shall be 0b1",
                                disp="shf")

PID = CCSDSKey(                 name='pid',
                                start=5,
                                l=4,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="The unique id of the sub-process or task that issued the packet. See external table 'apidDescription'",
                                disp="pid")

LEVELFLAG = CCSDSKey(           name='level_flag',
                                dic={0: '0', 1: '1'},
                                start=9,
                                l=1,
                                verbose="If the packet is not payload, what software is it? Shall be 0d0 if the payload flag is 0b1, else shall be 0b0 if the packet is L0-related or 0b1 for L1",
                                disp="lvl")

PAYLOADFLAG = CCSDSKey(         name='payload_flag',
                                dic={0: '0', 1: '1'},
                                start=10,
                                l=1,
                                verbose="Is that a packet routed from/to the payload? Shall be 0b1 if yes or 0b0 if no",
                                disp="pld")

PACKETCATEGORY = CCSDSKey(      name='packet_category',
                                start=11,
                                l=5,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="Defines the auxiliary header structure for telemetry packets (see external table 'packetCategoryDescription'). Unused for telecommands (set at 0b0000)",
                                disp="cat")

SEQUENCEFLAG = CCSDSKey(        name='sequence_flag',
                                dic={'segment': '00', 'start': '01',
                                     'end': '10', 'standalone': '11'},
                                start=16,
                                l=2,
                                dic_force='standalone',
                                non_db_dic=True,
                                verbose="The stand-alone or continuation status of a packet. Always stand-alone, shall be 0b11",
                                disp="seq")

PACKETID = CCSDSKey(            name='packet_id',
                                start=18,
                                l=14,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="The incremented id of the packet. Will be looped once the maximum encode-able value is reached",
                                disp="#")

# this CCSDSKey must not be relative, i.e. there must be a "start" defined
# cf ccsdspacker.increment_data_length()
DATALENGTH = CCSDSKey(          name='data_length',
                                start=32,
                                l=16,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="The length, in octet, of the secondary header + auxiliary header + data field",
                                disp="len")


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
    """
    verbose = "binary -> unsigned integer"
    """
    # apply a maximum to the rounded number of days from 1970 to the
    # maximum of gmtime
    return Day(min(24001, bincore.bin2int(v)))


def msec_unpack(v):
    """
    verbose = "binary -> unsigned integer"
    """
    # apply a maximum to the possible number of msec per day
    return Ms(min(86399999, bincore.bin2int(v)))


DAYSINCEREF_TELEMETRY = CCSDSKey(   name='days_since_ref',
                                    start=0,
                                    l=16,
                                    fctunpack=days_unpack,
                                    fctpack=bincore.int2bin,
                                    verbose="The integer number of fully elapsed days since the epoch reference",
                                    disp="days")

MSECSINCEREF_TELEMETRY = CCSDSKey(  name='ms_since_today',
                                    start=16,
                                    l=32,
                                    fctunpack=msec_unpack,
                                    fctpack=bincore.int2bin,
                                    verbose="The integer number of milli-seconds elapsed since previous midnight (UTC)",
                                    disp="ms")

# all keys in the right order
HEADER_S_KEYS_TELEMETRY = [DAYSINCEREF_TELEMETRY, MSECSINCEREF_TELEMETRY]
HEADER_S_KEYS_TELEMETRY = CCSDSTrousseau(HEADER_S_KEYS_TELEMETRY, octets=False)


# SECONDARY HEADER TELECOMMAND
# origin of start/end is end of primary header
# start/end units is bits


REQACKRECEPTIONTELECOMMAND = CCSDSKey(  name='reqack_reception',
                                        start=0,
                                        l=1,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of receipt?",
                                        disp="rack")

REQACKFORMATTELECOMMAND = CCSDSKey(     name='reqack_format',
                                        start=1,
                                        l=1,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of formatting?",
                                        disp="fack")

REQACKEXECUTIONTELECOMMAND = CCSDSKey(  name='reqack_execution',
                                        start=2,
                                        l=1,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of execution?",
                                        disp="eack")

TELECOMMANDID = CCSDSKey(               name='telecommand_id',
                                        start=3,
                                        l=10,
                                        fctunpack=bincore.bin2int,
                                        fctpack=bincore.int2bin,
                                        verbose="The id of the telecommand sent",
                                        disp="tcid")

EMITTERID = CCSDSKey(                   name='user_id',
                                        start=13,
                                        l=3,
                                        fctunpack=bincore.bin2int,
                                        fctpack=bincore.int2bin,
                                        verbose="The id of the antena/program/script responsible for the telecommand",
                                        disp="user")

SIGNATURE = CCSDSKey(                   name='signature',
                                        start=16,
                                        l=128,
                                        fctunpack=bincore.bin2hex,
                                        fctpack=bincore.hex2bin,
                                        verbose="The cryptographic hash using the public/private key system",
                                        disp='sign')

HEADER_S_KEYS_TELECOMMAND = [REQACKRECEPTIONTELECOMMAND,
    REQACKFORMATTELECOMMAND, REQACKEXECUTIONTELECOMMAND, TELECOMMANDID,
    EMITTERID, SIGNATURE]
HEADER_S_KEYS_TELECOMMAND = CCSDSTrousseau(HEADER_S_KEYS_TELECOMMAND,
                                            octets=False)


def disp(**hd):
    res = []
    res += ["V:{ccsds_version} T:{packet_type} SHF:{secondary_header_flag} "\
            "PLD:{payload_flag} LVL:{level_flag} PID:{pid} CAT:{packet_category} "\
            " SF:{sequence_flag} #:{packet_id} len:{data_length}".format(**hd)]
    res += ["Ds:{days_since_ref} Ms:{ms_since_today}".format(**hd)]
    return "\n".join(res)
