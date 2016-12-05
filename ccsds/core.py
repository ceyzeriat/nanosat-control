#!/usr/bin/env python
# -*- coding: utf-8 -*-


import binascii
import .ccsdsexception


def int2bin(i, pad=8):
    """
    Give an int ``i`` as int or str, get bits
    Optionnally pad to ``pad`` characters (default is 8).
    Set `pad`` to ``None`` or ``False`` for no padding.
    """
    iint = int(i)
    res = str(i) if iint<=1 else bin(iint>>1)[2:] + str(iint&1)
    if pad not in ['False', 0, '0', None] and isinstance(pad, int):
        return "{:0>{pad}}".format(res, pad=pad)
    else:
        return res

def bin2int(b):
    """
    Give bits ``b`` as str or '0b001', get an int
    """
    return int(b, 2) if isinstance(b, str) else b

def bin2hex(b, char=False):
    """
    Give bits ``b`` as str or '0b001', get hex
    The hex returned will be a single char if ``char`` is True or
    a len=2 string 'ff' if not
    """
    if char:
        return chr(int(b, 2)) if isinstance(b, str) else chr(b)
    else:    
        return "{:02X}".format(int(b, 2) if isinstance(b, str) else b)

def hex2bin(h, pad=8):
    """
    Give hex ``h`` as char, 'ff' or '0xff', returns bits
    """
    return int2bin(hex2int(h), pad=pad)

def hex2int(h):
    """
    Give hex ``h`` as char, 'ff' or '0xff', returns int
    """
    return int(h, 16) if len(h) > 1 else ord(h)

def int2hex(i, char=False):
    """
    Give an int, returns a char if ``char`` is True or
    'ff' if not.
    """
    return chr(i) if char else int2bin(bin2hex(i))

def octify(b):
    """
    Splits a long ``b`` octets sequence into 8-bit pieces
    """
    return [b[i:i+8] for i in range(0, len(b), 8)]
