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
import numpy as np
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
from . import ctrlexception
from .prepare_param import *


# make sure that python 3 understands unicode native python 2 function
if PYTHON3:
    unicode = str


def prepare_terminal(txt):
    os.system("reset")
    #set_term_title("{}".format(txt))
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
                    re.sub(r'_([a-z])', lambda m: m.group(1).upper(), txt[1:]))
    return inflect.engine().singular_noun(camelize)

def get_pid():
    """
    Returns the process ID number of the invoking thread
    """
    return current_process().pid

def append_logfile(message):
    """
    Appends message at the end of the log file, with a timestamp
    """
    f = open(LOGFILE, mode="a")
    f.write('{} {}\n'.format(now().strftime('%Y/%m/%d %H:%M:%S'), message))
    f.close()

def split_flow(data, n=1):
    """
    Splits and returns the ccsds packets if one expects a frames-flow
    """
    if not FRAMESFLOW:
        raise ctrlexception.NotInFramesFlow()
    # split CCSDS using the special split chars
    if not AX25ENCAPS:
        res = Byt(data).split(CCSDSSPLITCHAR*2, n)
        for idx, item in enumerate(res[:n]):
            if len(item) <= 0:
                continue
            res[idx] = item.replace(CCSDSSPLITCHAR+CCSDSESCAPECHAR,
                                    CCSDSSPLITCHAR)
        return res
    # split KISS using the special split chars
    elif KISSENCAPS:
        raise ctrlexception.NotImplemented("Frames-FLow with KISS")
    else:
        raise ctrlexception.CantRunAX25FramesFlow()

def merge_flow(datalist):
    """
    Merges the ccsds packets contained in datalist if one expects a
    frames-flow
    """
    if not FRAMESFLOW:
        raise ctrlexception.NotInFramesFlow()
    # merge CCSDS using the special split chars
    if not AX25ENCAPS:
        return (CCSDSSPLITCHAR*2).join([
                    Byt(item).replace(CCSDSSPLITCHAR,
                                        CCSDSSPLITCHAR+CCSDSESCAPECHAR)\
                        for item in datalist if len(item) > 0])\
                + CCSDSSPLITCHAR*2
    # merge KISS using the special split chars
    elif KISSENCAPS:
        raise ctrlexception.NotImplemented("Frames-FLow with KISS")
    else:
        raise ctrlexception.CantRunAX25FramesFlow()

def split_socket_info(data, asStr=False):
    """
    Splits the data using the socket separator and returns a dictionnary
    of the different pieces in bytes format
    """
    res = map(Byt, data.split(SOCKETSEPARATOR*2))
    res = [map(Byt, item.replace(SOCKETSEPARATOR+SOCKETESCAPE,SOCKETSEPARATOR)\
                        .split(SOCKETMAPPER, 1))\
                            for item in res]
    dic = {}
    for k, v in res:
        dic[str(k)] = str(v) if asStr else v
    return dic

def merge_socket_info(**kwargs):
    """
    Merges the data using the socket separator and returns a string
    """
    res = []
    for k, v in kwargs.items():
        if not isStr(v):
            v = str(v)
        res.append(Byt(k) + SOCKETMAPPER + Byt(v))
    return (SOCKETSEPARATOR*2).join([
                item.replace(SOCKETSEPARATOR, SOCKETSEPARATOR+SOCKETESCAPE)\
                    for item in res])

def merge_reporting(**kwargs):
    """
    Merges the data using the socket separator and returns a string
    """
    kwargs[REPORTKEY] = Byt(1)
    return merge_socket_info(**kwargs)

def is_reporting(data):
    """
    Returns ``True`` if the data is some reporting
    """
    lrep = len(REPORTKEY)
    lmap = len(SOCKETMAPPER)
    socksep = SOCKETSEPARATOR * 2
    lsep = len(socksep)
    PROOF = Byt(REPORTKEY) + SOCKETMAPPER + Byt(1)
    # only and just reporting flag
    if data == PROOF:
        return True
    # start with report flag
    elif data[:lrep+lsep+lmap+1] == PROOF + socksep:
        return True
    # ends with report flag
    elif data[-(lrep+lsep+lmap+1):] == socksep + PROOF:
        return True
    elif data.find(socksep + PROOF + socksep) != -1:
        return True
    return False

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

def save_json_cmds(path, cmds):
    """
    Loads all the commands from the json file, given the path list
    """
    f = open(rel_dir(*path), mode='w')
    json.dump(cmds, f)
    f.close()

def strISOstamp2datetime(txt):
    """
    Tranforms a ISO date as string into a datetime
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
    dt += [int(ms.split('.')[0]), pytz.utc]
    return datetime.datetime(*dt)

def now():
    return datetime.datetime.now(pytz.utc)

def now2daystamp():
    return int(time.mktime(time.localtime())/86400.-DATETIME_REF)

def now2msstamp():
    g = now()
    return int(g.hour * 36e5 + g.minute * 6e4 + g.second * 1e3
                + g.microsecond//1000)

def stamps2time(daystamp, msstamp):
    ts = (DATETIME_REF+daystamp)*86400. + msstamp*0.001
    return datetime.datetime.fromtimestamp(ts, tz=pytz.utc)

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

def clean_name(txt):
    """
    Cleans the ``txt`` from non-alphanum characters; replaces the first
    character by a word if it is a number
    """
    if not isinstance(txt, (str, unicode)):
        raise TypeError("txt must be string or unicode")
    number = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
              "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    authorized = list(range(65, 91)) + list(range(97, 123))\
                    + list(range(48, 58)) + [95]
    txt = "".join([letter for letter in str(txt)
                        if (ord(letter) in authorized)])
    return number[txt[0]] + "_" if ord(txt[0]) in number.keys() else txt[0]\
            + txt[1:]

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
