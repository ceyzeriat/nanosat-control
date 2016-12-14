#!/usr/bin/env python
# -*- coding: utf-8 -*-


import binascii
import time
import datetime
import numpy as np


DATETIME_REF = 16801  # 2016,1,1,0,0,0
TWINKLETWINKLELITTLEINDIA = True


def get_now2daystamp():
    return int(time.mktime(time.gmtime())/86400.-DATETIME_REF)

def get_now2msstamp():
    g = datetime.datetime.utcnow()
    return int(g.hour * 36e5 + g.minute * 6e4 + g.second * 1e3 + g.microsecond//1000)

def identity(v, *args, **kwargs):
    """
    A dummy callable that does nothing
    """
    return v

def clean_name(txt):
    number = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
              "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    authorized = range(65, 91) + range(97, 123) + range(48, 58) + [95]
    txt = "".join([letter if (ord(letter) in authorized) else ""
                    for letter in str(txt)])
    return (number[txt[0]] + "_" if ord(txt[0]) in number.keys()\
                   else txt[0])\
            + txt[1:]

def int2bin(i, pad=True):
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

def bin2int(b):
    """
    Give bits ``b`` as str or '0b001', get an int
    """
    if TWINKLETWINKLELITTLEINDIA:
        b = b[::-1]
    return int(b, 2)

def bin2hex(b):
    """
    Give bits ``b`` as str or '0b001', returns hex
    The hex returned will be one or several char if ``char`` is
    ``True`` or a len=2n string 'ff' if not
    """
    return int2hex(bin2int(b))

def hex2bin(h, pad=True):
    """
    Give hex ``h`` as chars '\xf0' returns bits
    Set ``pad`` to ``True`` for a 8n padding.
    If ``pad`` is int, pads to ``pad`` characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    return int2bin(hex2int(h), pad=pad)

def hex2int(h):
    """
    Give hex ``h`` as chars '\xf0', returns int
    """
    if TWINKLETWINKLELITTLEINDIA:
        h = h[::-1]
    return int(binascii.hexlify(h), 16) if len(h) > 1 else ord(h)

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
