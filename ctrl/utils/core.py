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
from . import ctrlexception
from .prepare_param import *
from .byt import Byt
#from IPython.utils.terminal import toggle_set_term_title, set_term_title
#toggle_set_term_title(True)

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

def split_socket_info(data, asStr=False):
    """
    Splits the data using the socket separator and returns a dictionnary
    of the different pieces in bytes format
    """
    res = map(Byt, re.split(str(RESPLITVARS), str(data)))
    res = [map(Byt, re.split(   str(RESPLITMAP),
                                str(item.replace(SOCKETESCAPE+SOCKETSEPARATOR,
                                                    SOCKETSEPARATOR))
                            )) for item in res]
    dic = {}
    if asStr:
        for k, v in res:
            dic[str(Byt(k))] = str(v.replace(SOCKETESCAPE+SOCKETMAPPER,
                                                    SOCKETMAPPER))
    else:
        for k, v in res:
            dic[str(Byt(k))] = v.replace(SOCKETESCAPE+SOCKETMAPPER,
                                            SOCKETMAPPER)
    return dic

def merge_socket_info(**kwargs):
    """
    Merges the data using the socket separator and returns a string
    """
    res = []
    for k, v in kwargs.items():
        if not isStr(v):
            v = str(v)
        v = Byt(v)
        v = v.replace(SOCKETMAPPER, SOCKETESCAPE+SOCKETMAPPER)
        res.append(Byt(k) + SOCKETMAPPER + v)
    return SOCKETSEPARATOR.join([
                item.replace(SOCKETSEPARATOR,
                                SOCKETESCAPE+SOCKETSEPARATOR) for item in res])

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
    lsep = len(SOCKETSEPARATOR)
    PROOF = Byt(REPORTKEY) + SOCKETMAPPER + Byt(1)
    # only and just reporting flag
    if data == PROOF:
        return True
    # start with report flag
    elif data[:lrep+lsep+lmap+1] == PROOF + SOCKETSEPARATOR:
        return True
    # ends with report flag
    elif data[-(lrep+lsep+lmap+1):] == SOCKETSEPARATOR + PROOF:
        return True
    elif data.find(SOCKETSEPARATOR + PROOF + SOCKETSEPARATOR) != -1:
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
    return parser.parse(txt)

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

def int2bin(i, pad=True, **kwargs):
    """
    Give an int ``i`` as int or str, returns bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    int2bin.verbose = "-> binary"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    i = int(i)
    if i < 0:
        raise ctrlexception.NegativeUnsignedInteger(i)
    if i <= 1:
        b = str(i)
    else:
        b = bin(i>>1)[2:] + str(i&1)
    # 8n padding
    if pad is True:
        b = b.zfill(((len(b)-1)//8+1)*8)
    # padding to pad int value
    elif pad not in ['False', 0, '0', None] and isinstance(pad, int):
        b = "{:0>{pad}}".format(b, pad=pad)
    if litFucInd:
        return b[::-1]
    else:
        return b

def intSign2bin(i, sz, **kwargs):
    """
    Give a signed int ``i`` as int or str with its size ``sz`` in
    octet, returns bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    intSign2bin.verbose = "-> binary"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    sz = int(sz)*8
    i = int(i)
    half = 2**(sz-1)
    if not -half <= i <= half-1:
        raise ctrlexception.OutofboundInteger(i, sz//8)
    if i >= 0:
        return int2bin(i, pad=sz)
    else:
        if litFucInd:
            return int2bin(half+i, pad=sz)[:-1] + '1'
        else:
            return '1' + int2bin(half+i, pad=sz)[1:]

def bin2int(b, **kwargs):
    """
    Give bits ``b`` as str or '0b001', returns int
    """
    bin2int.verbose = "-> unsigned integer"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if litFucInd:
        b = b[::-1]
    return int(b, 2)

def bin2intSign(b, **kwargs):
    """
    Give bits ``b`` as str or '0b001', returns signed int
    """
    bin2intSign.verbose = "-> signed integer"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if litFucInd:
        b = b[::-1]
    if len(b) == 1:
        return int(b)
    elif int(b[0]) == 0:
        return int(b, 2)
    else:
        return int(b[1:], 2) - 2**(len(b)-1)

def bin2hex(b, pad=0, **kwargs):
    """
    Give bits ``b`` as str or '0b001', returns chars
    """
    bin2hex.verbose = "-> hexadecimal"
    return int2hex(bin2int(b), pad=pad)

def hex2bin(h, pad=True, **kwargs):
    """
    Give hex ``h`` as chars '\xf0' returns bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    hex2bin.verbose = "-> unsigned integer"
    return int2bin(hex2int(h), pad=pad)

def hex2int(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns int
    """
    hex2int.verbose = "-> unsigned integer"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if len(h) == 1:
        return ord(h)
    if litFucInd:
        h = h[::-1]
    return int(binascii.hexlify(Byt(h)), 16)

def hex2intSign(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns signed int
    """
    hex2intSign.verbose = "-> signed integer"
    i = hex2int(h)
    half = 2**(len(h)*8-1)
    if i < half:
        return i
    else:
        return i-2*half

def int2hex(i, pad=0, **kwargs):
    """
    Give an int, returns chars
    """
    int2hex.verbose = "-> hexadecimal"
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    hx = hex(i)[2:].replace('L', '')  # replace if long int
    hx = Byt(binascii.unhexlify(('0' * (len(hx) % 2)) + hx))
    if litFucInd:
        hx = hx[::-1]
    if pad > 1:
        hx = padit(txt=hx, l=pad, ch=Byt(0))
    return hx

def intSign2hex(i, sz):
    """
    Give a signed int ``i`` as int or str with its size ``sz`` in
    octet, returns chars
    """
    intSign2hex.verbose = "-> hexadecimal"
    sz = int(sz)
    i = int(i)
    half = 2**(sz*8-1)
    if not -half <= i <= half-1:
        raise ctrlexception.OutofboundInteger(i, sz//8)
    if i >= 0:
        return int2hex(i, pad=sz)
    else:
        return int2hex(2*half+i, pad=sz)

def reverse_if_little_endian(bits, **kwargs):
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if litFucInd:
        return bits[::-1]
    else:    
        return bits

def octify(b):
    """
    Splits a long ``b`` bits sequence into 8-bit pieces
    after it has padded ``b`` to a 8n length
    """
    b = padit(b, ((len(b)-1)//8+1)*8, '0')
    return [b[i:i+8] for i in range(0, len(b), 8)]

def padit(txt, l, ch, **kwargs):
    """
    Pads with ``ch`` up to length ``l``, on the right is little endian
    or on the left if big
    ``txt`` and ``ch`` must be the same type (bytes or str)
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if litFucInd:
        return txt + ch * (l - len(txt))
    else:    
        return ch * (l - len(txt)) + txt

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
