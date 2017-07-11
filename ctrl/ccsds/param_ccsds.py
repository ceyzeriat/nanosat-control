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


from param import param_all
from .ccsdstrousseau import CCSDSTrousseau
from .ccsdskey import CCSDSKey
from ..utils import bincore
from ..utils import b
from ..utils import O
from ..utils.day import Day
from ..utils.ms import Ms


MAXIMUMDATALENGTH = 65536  # octets
MAXIMUMPACKETLENGTH = MAXIMUMDATALENGTH + 6  # octets

# length of packet as recorded in ccsds - LENGTHMODIFIER =
#   real length of Packet - length of Primary Header
# the official CCSDS standard specifies LENGTHMODIFIER = 1
LENGTHMODIFIER = 0


# PRIMARY HEADER
# origin of start/end is start of packet
# start/end units is bits

TELEMETRYTYPEID = 0
TELECOMMANDTYPEID = 1
SEQSEGMENT = 0
SEQSTART = 1
SEQEND = 2
SEQSTANDALONE = 3


PACKETVERSION = CCSDSKey(       name='ccsds_version',
                                dic={0: '000'},
                                start=0*b,
                                l=3*b,
                                dic_force=0,
                                verbose="The CCSDS format version. Shall be 0b000",
                                disp="v")

PACKETTYPE = CCSDSKey(          name='packet_type',
                                dic={TELEMETRYTYPEID: '0', TELECOMMANDTYPEID: '1'},
                                start=3*b,
                                l=1*b,
                                verbose="Whether telecommand packet or telemetry packet. Shall be 0b0 for telemetry or 0b1 for telecommand",
                                disp="tc")

SECONDARYHEADERFLAG = CCSDSKey( name='secondary_header_flag',
                                dic={0: '0', 1: '1'},
                                start=4*b,
                                l=1*b,
                                dic_force=1,
                                verbose="Is there a secondary header? Always true, shall be 0b1",
                                disp="shf")

PID = CCSDSKey(                 name='pid',
                                start=5*b,
                                l=4*b,
                                typ='uint',
                                verbose="The unique id of the sub-process or task that issued the packet. See external table 'apidDescription'",
                                disp="pid")

LEVELFLAG = CCSDSKey(           name='level_flag',
                                dic={0: '0', 1: '1'},
                                start=9*b,
                                l=1*b,
                                verbose="If the packet is not payload, what software is it? Shall be 0d0 if the payload flag is 0b1, else shall be 0b0 if the packet is L0-related or 0b1 for L1",
                                disp="lvl")

PAYLOADFLAG = CCSDSKey(         name='payload_flag',
                                dic={0: '0', 1: '1'},
                                start=10*b,
                                l=1*b,
                                verbose="Is that a packet routed from/to the payload? Shall be 0b1 if yes or 0b0 if no",
                                disp="pld")

PACKETCATEGORY = CCSDSKey(      name='packet_category',
                                start=11*b,
                                l=5*b,
                                typ='uint',
                                verbose="Defines the auxiliary header structure for telemetry packets (see external table 'packetCategoryDescription'). For Telecommands, set at 0 or 1",
                                disp="cat")

SEQUENCEFLAG = CCSDSKey(        name='sequence_flag',
                                dic={SEQSEGMENT: '00', SEQSTART: '01',
                                     SEQEND: '10', SEQSTANDALONE: '11'},
                                start=16*b,
                                l=2*b,
                                dic_force=SEQSTANDALONE,
                                verbose="The stand-alone or continuation status of a packet. Always stand-alone, shall be 0b11",
                                disp="seq")

PACKETID = CCSDSKey(            name='packet_id',
                                start=18*b,
                                l=14*b,
                                typ='uint',
                                verbose="The incremented id of the packet. Will be looped once the maximum encode-able value is reached",
                                disp="#")

# this CCSDSKey must not be relative, i.e. there must be a "start" defined
# cf ccsdspacker.increment_data_length()
DATALENGTH = CCSDSKey(          name='data_length',
                                start=32*b,
                                l=16*b,
                                typ='uint',
                                verbose="The length, in octet, of the secondary header + auxiliary header + data field",
                                disp="len")


# all keys in the right order
HEADER_P_KEYS = [PACKETVERSION, PACKETTYPE, SECONDARYHEADERFLAG, PAYLOADFLAG,
    LEVELFLAG, PID, PACKETCATEGORY, SEQUENCEFLAG, PACKETID, DATALENGTH]
HEADER_P_KEYS = CCSDSTrousseau(HEADER_P_KEYS)


# SECONDARY HEADER TELEMETRY
# origin of start/end is end of primary header
# start/end units is bits


# length of the bit sequence useful to unambiguously determine the
# beginning of a packet
AUTHPACKETLENGTH = 11


def days_unpack(v):
    """
    type = unsigned integer
    verbose = binary -> unsigned integer
    """
    # apply a maximum to the rounded number of days from 1970 to the
    # maximum of gmtime
    return Day(min(24001, v))


def msec_unpack(v):
    """
    type = unsigned integer
    verbose = binary -> unsigned integer
    """
    # apply a maximum to the possible number of msec per day
    return Ms(min(86399999, v))


DAYSINCEREF_TELEMETRY = CCSDSKey(   name='days_since_ref',
                                    start=0*O,
                                    l=2*O,
                                    typ='uint',
                                    fctfix=days_unpack,
                                    verbose="The integer number of fully elapsed days since the epoch reference",
                                    disp="days")

MSECSINCEREF_TELEMETRY = CCSDSKey(  name='ms_since_today',
                                    start=2*O,
                                    l=4*O,
                                    typ='uint',
                                    fctfix=msec_unpack,
                                    verbose="The integer number of milli-seconds elapsed since previous midnight (UTC)",
                                    disp="ms")

# all keys in the right order
HEADER_S_KEYS_TELEMETRY = [DAYSINCEREF_TELEMETRY, MSECSINCEREF_TELEMETRY]
HEADER_S_KEYS_TELEMETRY = CCSDSTrousseau(HEADER_S_KEYS_TELEMETRY)


# SECONDARY HEADER TELECOMMAND
# origin of start/end is end of primary header
# start/end units is bits


REQACKRECEPTIONTELECOMMAND = CCSDSKey(  name='reqack_reception',
                                        start=0*b,
                                        l=1*b,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of receipt?",
                                        disp="rack")

REQACKFORMATTELECOMMAND = CCSDSKey(     name='reqack_format',
                                        start=1*b,
                                        l=1*b,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of formatting?",
                                        disp="fack")

REQACKEXECUTIONTELECOMMAND = CCSDSKey(  name='reqack_execution',
                                        start=2*b,
                                        l=1*b,
                                        dic={0: '0', 1: '1'},
                                        verbose="Should the satellite return an acknowledgement of execution?",
                                        disp="eack")

TELECOMMANDID = CCSDSKey(               name='telecommand_id',
                                        start=3*b,
                                        l=10*b,
                                        typ='uint',
                                        verbose="The id of the telecommand sent",
                                        disp="tcid")

EMITTERID = CCSDSKey(                   name='user_id',
                                        start=13*b,
                                        l=3*b,
                                        typ='uint',
                                        verbose="The id of the antena/program/script responsible for the telecommand",
                                        disp="user")

SIGNATURE = CCSDSKey(                   name='signature',
                                        start=2*O,
                                        l=param_all.KEYLENGTHCCSDS*O,
                                        typ='byt',
                                        verbose="The cryptographic hash using the public/private key system",
                                        disp='sign')

HEADER_S_KEYS_TELECOMMAND = [REQACKRECEPTIONTELECOMMAND,
    REQACKFORMATTELECOMMAND, REQACKEXECUTIONTELECOMMAND, TELECOMMANDID,
    EMITTERID, SIGNATURE]
HEADER_S_KEYS_TELECOMMAND = CCSDSTrousseau(HEADER_S_KEYS_TELECOMMAND)
