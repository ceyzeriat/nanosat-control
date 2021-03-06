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


from sys import version_info
PYTHON3 = version_info > (3,)


import binascii
import time
import datetime
import os
import sys
import glob
import pytz
import re
import inflect
import json
from dateutil import parser
from multiprocessing import current_process
from byt import Byt
from sympy import solve, sympify


from . import ctrlexception as exc
from .posixutc import *
from .prepare_param import *


# make sure that python 3 understands unicode native python 2 function
if PYTHON3:
    unicode = str


def prepare_terminal(txt):
    ### os.system("reset")
    sys.stdout.write("\x1b]2;{}\x07".format(txt))

def get_tc_packet_id():
    """
    Just reads the packet id from the file
    """
    f = open(PACKETIDFULLFILE, mode='r')
    res = int(f.readline().strip())
    f.close()
    return res

def get_next_tc_packet_id():
    """
    Reads the packet id from the file and adds one
    """
    return (get_tc_packet_id()+1) % MAXPACKETID

def get_set_next_tc_packet_id():
    """
    Reads the packet id from the file, adds one and saves new value
    """
    v = get_next_tc_packet_id()
    f = open(PACKETIDFULLFILE, mode='w')
    f.write(str(v))
    f.close()
    return v

def camelize_singular(txt):
    """
    Produce a 'camelized' and singular class name.
    e.g. 'the_underscores' -> 'TheUnderscore'
    """
    camelize = str(txt[0].upper() +\
                    re.sub(r'_([a-z])',
                           lambda m: m.group(1).upper(), txt[1:]))
    return inflect.engine().singular_noun(camelize)

def camelize_singular_rev(txt):
    """
    Produce a 'decamelized' and plural class name.
    e.g. 'TheUnderscore' -> 'the_underscores'
    """
    decamelize = str(txt[0].lower() +\
                    re.sub(r'([A-Z])',
                           lambda m: '_'+m.group(1).lower(), txt[1:]))
    return inflect.engine().plural_noun(decamelize)

def get_pid():
    """
    Returns the process ID number of the invoking thread
    """
    return current_process().pid

def append_logfile(message):
    """
    Appends message at the end of the log file, with a timestamp

    Args:
      * message (str): the message to append
    """
    f = open(LOGFILE, mode="a")
    f.write('{} {}\n'.format(now().strftime(LOGFILETIMESTAMPFMT),
                             str(message)))
    f.close()

def recover_ccsds(data):
    """
    Recovers the un-escaped split characters

    Args:
      * data (str or list of str): the text to process
    """
    return data.replace(CCSDSESCAPEDSPLIT, CCSDSSPLITCHAR)

def split_ccsds(data, n):
    """
    Splits the ccsds according to the defined split ccsds character.
    Returns a list of size 1 at minimum, and ``n+1`` at maximum, which
    [-1] element is the remainder of the operation
    
    Args:
      * data (Byt): the bytes-chain to split
      * n (int): the maximum number of packets to split
    """
    return data.split(CCSDSSPLITCHAR*2, n)

def split_flow(data, n=-1):
    """
    Splits packets from flow if flow mode activated

    Args:
      * data (Byt): the data flow to split
      * n (int): how many packets should be splited, at maximum,
        set to -1 for all
    """
    if not FRAMESFLOW:
        raise exc.NotInFramesFlow()
    # split CCSDS using the special split chars
    if not AX25ENCAPS:
        res = split_ccsds(Byt(data), int(n))
        # no split found
        if len(res) < 2:
            return res
        # apply recovery of escaped chars to all splits found except last one
        return list(map(recover_ccsds, res[:-1])) + res[-1:]
    # split KISS using the special split chars
    elif KISSENCAPS:
        raise exc.NotImplemented("Frames-FLow with KISS")
    else:
        raise exc.NotImplemented("Unknown mode")

def merge_flow(datalist, trailingSplit=True):
    """
    Merges the packets if the flow mode is activated

    Args:
    * datalist (list of Byt): the packets to merge together
    * trailingSplit (bool): whether to add a trailing split character
    """
    if not FRAMESFLOW:
        raise exc.NotInFramesFlow()
    # merge CCSDS using the special split chars
    if not AX25ENCAPS:
        res = (CCSDSSPLITCHAR*2).join([
                    Byt(item).replace(CCSDSSPLITCHAR, CCSDSESCAPEDSPLIT)\
                        for item in datalist\
                            if len(item) > 0])
        if trailingSplit:
            res += CCSDSSPLITCHAR*2
        return res
    # merge KISS using the special split chars
    elif KISSENCAPS:
        raise exc.NotImplemented("Frames-FLow with KISS")
    else:
        raise exc.NotImplemented("Unknown mode")

def to_num(v):
    if not isStr(v):
        return v
    v = v.strip()
    try:
        v = int(v)
    except:
        if v[:2] == "0x":
            try:
                v = int(v, 16)
            except:
                pass
        elif v[:2] == "0b":
            try:
                v = int(v, 2)
            except:
                pass
        else:
            try:
                v = float(v)
            except:
                pass
    return v

def load_json_cmds(path):
    """
    Loads all the commands from the json file, given the path list
    """
    f = open(rel_dir(*path), mode='r')
    allcmds = json.load(f)
    f.close()
    return allcmds

def strISOstamp2datetime(txt):
    """
    Tranforms a ISO date string into a datetime
    """
    return parser.parse(str(txt))

def packetfilename2datetime(txt):
    """
    Give a filename following `TELEMETRYNAMEFORMAT`
    """
    txt = os.path.basename(txt)
    dd, ms = txt.split('_')[1:]
    dd, tt = dd.split('T')
    dt = [int(dd[:4]), int(dd[4:6]), int(dd[6:])]
    dt = dt + [int(tt[:2]), int(tt[2:4]), int(tt[4:])]
    dt += [int(ms.split('.')[0])]
    return PosixUTC(*dt)

def now():
    """
    Returns the now timestamp as datetime
    """
    return PosixUTC.now()

def now2daystamp():
    """
    Returns a day stamp for datetime t
    """
    return time2daystamp(now())

def now2msstamp():
    """
    Returns a milli-sec stamp for now
    """
    return time2msstamp(now())

def time2msstamp(t):
    """
    Returns a milli-sec stamp for datetime t
    """
    return int(t.hour * 36e5 + t.minute * 6e4 + t.second * 1e3
                + t.microsecond//1000)

def time2daystamp(t):
    """
    Returns a day stamp for now, or from t (PosixUTC)
    """
    return int(t.totimestamp()/86400.-DATETIME_REF)

def time2stamps(dt):
    """
    Give a PosixUTC, get ms and day stamps
    """
    return (time2msstamp(dt), time2daystamp(dt))

def stamps2time(daystamp, msstamp):
    """
    Give a day and a milli-sec stamp, return a datetime
    """
    ts = (DATETIME_REF+daystamp)*86400. + msstamp*0.001
    return PosixUTC.fromtimestamp(ts)

def identity(v, *args, **kwargs):
    """
    A dummy callable that does nothing
    """
    return v

def setstr(txt, slc, rep):
    """
    Sets ``rep`` at ``slc`` slice in ``txt``
    ``txt`` and ``rep`` must be the same type (bytes or str)
    """
    return txt[:slc.start] + rep[0:slc.stop-slc.start] + txt[slc.stop:]

authorized = list(range(65, 91)) + list(range(97, 123))\
                    + list(range(48, 58)) + [95]
def clean_name(txt, allow_front_digit=False, allow_space=False):
    """
    Cleans the ``txt`` from non-alphanum characters; replaces the first
    character by a word if it is a number
    """
    if not isinstance(txt, (str, unicode)):
        raise TypeError("txt must be string or unicode")
    number = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
              "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    space = [ord(' ') if allow_space else '']
    txt = "".join([letter for letter in str(txt)
                        if (ord(letter) in (authorized + space))])
    if allow_front_digit:
        return txt
    else:
        if txt[0] in number.keys():
            return number[txt[0]] + txt[1:]
        else:
            return txt

def isStr(txt):
    """
    Check if txt is valid string: (str, unicode, bytes)
    """
    return isinstance(txt, (str, unicode, bytes, Byt))

def fillit(txt, l, ch, right=True):
    """
    Fills ``txt`` on the ``right`` with char ``ch`` up to ``l`` length
    ``txt`` and ``ch`` must be the same type (bytes or str)
    """
    if right:
        return txt + ch*(l-len(txt))
    else:
        return ch*(l-len(txt)) + txt

def two_comp_uint(v, bits):
    """
    Give v the value as int and bits the number of bits on which it is
    encoded
    """
    return (1<<bits)-v-1

def crc32(message, crc=None):
    """
    Give a message, returns a CRC on 4 octet using
    basecrc as crc start-value (if given)
    """
    crc = 0xffffffff if crc is None else int(crc)
    for byte in Byt(message).iterInts():
        crc = (crc >> 8) ^ CRC32TABLE[(crc ^ byte) & 0xFF]
    return two_comp_uint(crc, 32)


def payload_crc32(message):
    """
    code to compute fucking stm32 non-standard crc with standard polynomial
    """
    crc = 0xffffffff
    for i in Byt(message).iterInts():
        b = [(i >> 24) & 0xFF, (i >> 16) & 0xFF, (i >> 8) & 0xFF, i & 0xFF]
        for byte in b:
            crc = ((crc << 8) & 0xffffffff) ^ payload_crc_table[(crc >> 24) ^ byte]
    return crc


def inverse_eqn(eqn):
    """
    Inverse a symbolic expression with variable x
    Keeps x as the variable in the inverted expression
    > inverse('4*x/2')
    'y = x/2'
    """
    e = sympify('-x + ' + eqn.replace('x', 'y'))
    return str(solve(e, 'y')[0]).replace('x', 'float(x)')
