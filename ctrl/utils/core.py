#!/usr/bin/env python
# -*- coding: utf-8 -*-


import binascii
import time
import datetime
import numpy as np
import os
import glob
import pytz
import re
import inflect
from dateutil import parser
from . import ctrlexception
from ..param.param_all import *


# make sure that python 3 understands unicode native python 2 function
try:
    PYTHONVERSION = 2
    _DUM = bool(type(unicode))
except:
    PYTHONVERSION = 3
    unicode = str


MAXPACKETID = 2**14

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME = os.path.expanduser("~")

def concat_dir(*args):
    return os.path.join(*args)

def rel_dir(*args):
    return concat_dir(ROOT, *args)

TELEMETRYDUMPFOLDER = concat_dir(HOME, *TELEMETRYDUMPFOLDER)
if not os.path.exists(TELEMETRYDUMPFOLDER):
    if NOERRORATIMPORT:
        print(ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER))
    else:
        raise ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER)

try:
    f = open(rel_dir(*DBFILE), mode='r')
    DBENGINE = f.readline().strip()
    assert len(DBENGINE) > 20
    assert DBENGINE[:13] == 'postgresql://'
    f.close()
except IOError:
    if NOERRORATIMPORT:
        print(ctrlexception.MissingDBServerFile(rel_dir(*DBFILE)))
    else:
        raise ctrlexception.MissingDBServerFile(rel_dir(*DBFILE))

def get_tc_packet_id():
    f = open(rel_dir(*PACKETIDFILE), mode='r')
    res = int(f.readline().strip())
    f.close()
    return res

def get_next_tc_packet_id():
    return (get_tc_packet_id()+1) % MAXPACKETID

def get_set_next_tc_packet_id():
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
    camelize = str(txt[0].upper() + \
            re.sub(r'_([a-z])', lambda m: m.group(1).upper(), txt[1:]))
    return inflect.engine().singular_noun(camelize)

def split_socket(data):
    """
    Splits the data using the socket separator and returns a list of
    the different pieces
    """
    res = []
    spot = 0
    data = str(data)
    while spot != -1:
        spot = data.find(core.SOCKETSEPARATOR)
        if spot == -1:
            res.append(data)
        else:
            res.append(data[:spot])
        data = data[spot + len(core.SOCKETSEPARATOR):]
    return res

def merge_socket(*args):
    """
    Merges the data using the socket separator and returns a string
    """
    return core.SOCKETSEPARATOR.join(['{}'.format(item) for item in args])

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

def strISOstamp2datetime(txt):
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
    return txt[:slc.start] + rep[0:slc.stop-slc.start] + txt[slc.stop:]

def clean_name(txt):
    number = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
              "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    authorized = list(range(65, 91)) + list(range(97, 123))\
                    + list(range(48, 58)) + [95]
    txt = "".join([letter if (ord(letter) in authorized) else ""
                    for letter in str(txt)])
    return (number[txt[0]] + "_" if ord(txt[0]) in number.keys()\
                   else txt[0])\
            + txt[1:]

def isStr(txt):
    """
    Check if txt is valid string
    """
    return isinstance(txt, (str, unicode))

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
    if not isinstance(h, bytes) and PYTHONVERSION == 3:
        h = bytes([ord(item) for item in h])
    return int(binascii.hexlify(h), 16)

def int2hex(i, pad=0):
    """
    Give an int, returns string of chars
    """
    hx = hex(i)[2:].replace('L', '')  # replace if long int
    hx = binascii.unhexlify(('0' * (len(hx) % 2)) + hx)
    if TWINKLETWINKLELITTLEINDIA:
        hx = hx[::-1]
    if pad > 1:
        hx = padit(hx, pad, '\x00')
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
    b = str(b).zfill(((len(b)-1)//8+1)*8)
    return [b[i:i+8] for i in range(0, len(b), 8)]

def padit(txt, l, ch='0'):
    """
    Pads with ``ch`` up to length ``l``, on the right is little endian
    or on the left if big
    """
    if TWINKLETWINKLELITTLEINDIA:
        return txt + ch[0] * (l - len(txt))
    else:    
        return ch[0] * (l - len(txt)) + txt
