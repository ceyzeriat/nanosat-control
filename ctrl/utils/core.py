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
import glob
import pytz
import re
import inflect
import json
from dateutil import parser
from multiprocessing import current_process
from sys import stdout
from . import ctrlexception
from ..param.param_all import *


# make sure that python 3 understands unicode native python 2 function
if PYTHON3:
    unicode = str

MAXPACKETID = 2**14

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME = os.path.expanduser("~")

def concat_dir(*args):
    """
    Concatenates the path in ``args`` into a string-path
    """
    return os.path.join(*args)

def rel_dir(*args):
    """
    Concatenates the path in ``args`` into a relative
    string-path from the package directory
    """
    return concat_dir(ROOT, *args)

TELEMETRYDUMPFOLDER = concat_dir(HOME, *TELEMETRYDUMPFOLDER)
if not os.path.exists(TELEMETRYDUMPFOLDER):
    if NOERRORATIMPORT:
        print(ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER))
    else:
        raise ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER)

# preparing the DB server
try:
    f = open(rel_dir(*DBFILE), mode='r')
    DBENGINE = f.readline().strip()
    f.close()
    assert len(DBENGINE) > 20
    assert DBENGINE[:13] == 'postgresql://'
except IOError:
    if NOERRORATIMPORT:
        print(ctrlexception.MissingDBServerFile(rel_dir(*DBFILE)))
    else:
        raise ctrlexception.MissingDBServerFile(rel_dir(*DBFILE))

# preparing the source callsign
try:
    f = open(rel_dir(*CSSOURCEFILE), mode='r')
    CSSOURCE = f.readline().strip()
    f.close()
except IOError:
    CSSOURCE = None
    if NOERRORATIMPORT:
        print(ctrlexception.MissingSourceCallsign(rel_dir(*CSSOURCEFILE)))
    else:
        raise ctrlexception.MissingSourceCallsign(rel_dir(*CSSOURCEFILE))

# preparing the destination callsign
try:
    f = open(rel_dir(*CSDESTFILE), mode='r')
    CSDESTINATION = f.readline().strip()
    f.close()
except IOError:
    CSDESTINATION = None
    if NOERRORATIMPORT:
        print(ctrlexception.MissingDestinationCallsign(rel_dir(*CSDESTFILE)))
    else:
        raise ctrlexception.MissingDestinationCallsign(rel_dir(*CSDESTFILE))


ART = """
  ____  _      ____        _   
 |  _ \(_) ___/ ___|  __ _| |_ 
 | |_) | |/ __\___ \ / _` | __|
 |  __/| | (__ ___) | (_| | |_ 
 |_|   |_|\___|____/ \__,_|\__|
                               
"""

def get_tc_packet_id():
    """
    Just reads the packet id from the file
    """
    f = open(rel_dir(*PACKETIDFILE), mode='r')
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
    f = open(rel_dir(*PACKETIDFILE), mode='w')
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
    res = re.split(RESPLITVARS, data)
    res = [re.split(RESPLITMAP,
                item.replace(SOCKETESCAPE+SOCKETSEPARATOR, SOCKETSEPARATOR))
            for item in res]
    dic = {}
    if asStr:
        for k, v in res:
            dic[bytes2str(k)] = bytes2str(v.replace(SOCKETESCAPE+SOCKETMAPPER,
                                                      SOCKETMAPPER))
    else:
        for k, v in res:
            dic[bytes2str(k)] = v.replace(SOCKETESCAPE+SOCKETMAPPER,
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
        v = str2bytes(v)
        v = v.replace(SOCKETMAPPER, SOCKETESCAPE+SOCKETMAPPER)
        res.append(str2bytes(k) + SOCKETMAPPER + v)
    return SOCKETSEPARATOR.join([
                item.replace(SOCKETSEPARATOR,
                                SOCKETESCAPE+SOCKETSEPARATOR) for item in res])

def merge_reporting(**kwargs):
    """
    Merges the data using the socket separator and returns a string
    """
    kwargs[REPORTKEY] = '1'
    return merge_socket_info(**kwargs)

def is_reporting(data):
    """
    Returns ``True`` if the data is some reporting
    """
    lrep = len(REPORTKEY)
    lmap = len(SOCKETMAPPER)
    lsep = len(SOCKETSEPARATOR)
    PROOF = str2bytes(REPORTKEY) + SOCKETMAPPER + b'1'
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
    return isinstance(txt, (str, unicode, bytes))

def int2bin(i, pad=True, **kwargs):
    """
    Give an int ``i`` as int or str, get bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    i = int(i)
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
    if TWINKLETWINKLELITTLEINDIA:
        return b[::-1]
    else:
        return b

def bin2int(b, **kwargs):
    """
    Give bits ``b`` as str or '0b001', get an int
    """
    if TWINKLETWINKLELITTLEINDIA:
        b = b[::-1]
    return int(b, 2)

def bin2hex(b, pad=0, **kwargs):
    """
    Give bits ``b`` as str or '0b001', returns hex
    The hex returned will be one or several char if ``char`` is
    ``True`` or a len=2n string 'ff' if not
    """
    return int2hex(bin2int(b), pad=pad)

def hex2bin(h, pad=True, **kwargs):
    """
    Give hex ``h`` as chars '\xf0' returns bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    return int2bin(hex2int(h), pad=pad)

def hex2int(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns int
    """
    if len(h) == 1:
        return ord(h)
    if TWINKLETWINKLELITTLEINDIA:
        h = h[::-1]
    return int(binascii.hexlify(str2bytes(h)), 16)

def int2hex(i, pad=0):
    """
    Give an int, returns string of chars
    """
    hx = hex(i)[2:].replace('L', '')  # replace if long int
    hx = binascii.unhexlify(('0' * (len(hx) % 2)) + hx)
    if TWINKLETWINKLELITTLEINDIA:
        hx = hx[::-1]
    if pad > 1:
        hx = padit(txt=hx, l=pad, ch=b'\x00')
    return hx

def reverse_if_little_endian(bits):
    if TWINKLETWINKLELITTLEINDIA:
        return bits[::-1]
    else:    
        return bits

def octify(b):
    """
    Splits a long ``b`` octets sequence into 8-bit pieces
    after it has padded ``b`` to a 8n length
    """
    b = b.zfill(((len(b)-1)//8+1)*8)
    return [b[i:i+8] for i in range(0, len(b), 8)]

def padit(txt, l, ch):
    """
    Pads with ``ch`` up to length ``l``, on the right is little endian
    or on the left if big
    ``txt`` and ``ch`` must be the same type (bytes or str)
    """
    if TWINKLETWINKLELITTLEINDIA:
        return txt + ch * (l - len(txt))
    else:    
        return ch * (l - len(txt)) + txt

def prepare_terminal(txt):
    __import__('os').system("reset")
    stdout.write("\x1b]2;{}\x07".format(txt))

def fillit(txt, l, ch, right=True):
    """
    Fills ``txt`` on the ``right`` with char ``ch`` up to ``l`` length
    ``txt`` and ``ch`` must be the same type (bytes or str)
    """
    if right:
        return txt + ch*(l-len(txt))
    else:
        return ch*(l-len(txt)) + txt

def str2bytes(txt):
    """
    Transforms whatever string or bytes into a ascii-bytes
    chain compatible with python 2 and 3
    """
    if isinstance(txt, int) and PYTHON3:
        return bytes([txt])
    elif not isinstance(txt, bytes) and PYTHON3:
        txt = bytes([ord(item) for item in txt])
    return txt

def str2ints(txt):
    """
    Transforms whatever string or bytes into a int-bytes
    chain compatible with python 2 and 3
    """
    if PYTHON3:
        if isinstance(txt, bytes):
            return txt
        elif not hasattr(txt, '__iter__'):
            return bytes([txt])
        else:
            return bytes([ord(item) for item in txt])
    else:
        return [ord(item) for item in txt]

def bytes2str(byt):
    """
    Transforms bytes to str
    """
    if not isinstance(byt, (str, unicode)):
        return str(byt.decode('utf-8'))
    else:
        return byt

def ints2str(ints):
    """
    Transforms whatever int-bytes chain into a string
    """
    if not hasattr(ints, '__iter__'):
        return chr(ints)
    return ''.join([chr(x) for x in ints])

def ints2bytes(ints):
    """
    Transforms whatever int-bytes chain into a string or bytes
    compatible with python 2 and 3
    """
    if PYTHON3:
        if not hasattr(ints, '__iter__'):
            return bytes([ints])
        else:
            return bytes([x for x in ints])
    else:
        return ints2str(ints)
