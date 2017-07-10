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


import binascii
from byt import Byt
import math
import struct
from . import ctrlexception


# little or big endian
TWINKLETWINKLELITTLEINDIA = False


def hex2str(v, **kwargs):
    """
    type = hexa string
    verbose = hexadecimal -> hexa string
    """
    return v.hex()


def str2hex(txt, pad=0, **kwargs):
    """
    A hexa-text '2F 3C A8' to bytes
    pad in hex chars
    type = hexadecimal
    verbose = hexa string -> hexadecimal
    """
    return padit(txt=Byt.fromHex(txt), l=pad, ch=Byt(0))


def bin2str(v, **kwargs):
    """
    type = hexa string
    verbose = binary -> hexa string
    """
    return bin2hex(v).hex()


def str2bin(txt, pad=True, **kwargs):
    """
    A hexa-text '2F 3C A8' to bytes
    pad in bits
    type = binary
    verbose = hexa string -> binary
    """
    return hex2bin(Byt.fromHex(txt), pad=pad)


def hex2txt(v, **kwargs):
    """
    type = hexa string
    verbose = hexadecimal -> message
    """
    return ''.join([chr(i) for i in v.ints() if i >= 32 and i <= 126])


def txt2hex(txt, pad=0, **kwargs):
    """
    A display-text [32--126] to bytes
    pad in hex chars
    type = hexadecimal
    verbose = message -> hexadecimal
    """
    txt = ''.join(Byt(i) for i in Byt(txt).ints()\
                                if i >= 32 and i <= 126)
    return padit(txt=txt, l=pad, ch=Byt(0))


def bin2txt(v, **kwargs):
    """
    type = message
    verbose = binary -> message
    """
    return hex2txt(bin2hex(v))

def txt2bin(txt, **kwargs):
    """
    type = binary
    verbose = message -> binary
    """
    return hex2bin(txt2hex(txt), pad=True)


def float2hex(v, pad=0, **kwargs):
    """
    Give a float32, returns chars
    pad in hex chars
    type = hexadecimal
    verbose = float32 -> hexadecimal
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    end = '<' if litFucInd else '>'
    v = Byt(struct.pack(end+'f', v))
    return padit(txt=v, l=pad, ch=Byt(0))

def hex2float(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns float32
    type = float32
    verbose = hexadecimal -> float32
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    end = '<' if litFucInd else '>'
    return struct.unpack(end+'f', h)


def double2hex(v, pad=0, **kwargs):
    """
    Give a float64, returns chars
    pad in hex chars
    type = hexadecimal
    verbose = float32 -> hexadecimal
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    end = '<' if litFucInd else '>'
    v = Byt(struct.pack(end+'d', v))
    return padit(txt=v, l=pad, ch=Byt(0))

def hex2double(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns float64
    type = float64
    verbose = hexadecimal -> float64
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    end = '<' if litFucInd else '>'
    return struct.unpack(end+'d', h)


def hex2hex(v, pad=0, **kwargs):
    """
    Give some hex, get some hex
    pad in hex chars
    type = hexadecimal
    verbose = Kept as hexadecimal
    """
    return padit(txt=v, l=pad, ch=Byt(0))


def bool2bin(i, **kwargs):
    """
    Give a boolean, returns a bin
    type = binary
    verbose = boolean -> binary
    """
    return str(int(i))

def bin2bool(i, **kwargs):
    """
    Give a binary, returns a bool
    type = boolean
    verbose = binary -> boolean
    """
    return bool(int(i))

def int2bin(i, pad=True, **kwargs):
    """
    Give an int ``i`` as int or str, returns bits
    Set ``pad`` to ``True`` for a 8n padding according to value.
    If ``pad`` is int, pads to ``pad`` bits.
    Set `pad`` to ``None`` or ``False`` for no padding.
    type = binary
    verbose = unsigned integer -> binary
    """
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
    octet, returns bits with the left-most bit being the sign-information
    type = binary
    verbose = signed integer -> binary
    """
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
    type = unsigned integer
    verbose = binary -> unsigned integer
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if litFucInd:
        b = b[::-1]
    return int(b, 2)

def bin2intSign(b, **kwargs):
    """
    Give bits ``b`` as str or '0b001', returns signed int
    type = signed integer
    verbose = binary -> signed integer
    """
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
    pad in hex chars
    type = hexadecimal
    verbose = binary -> hexadecimal
    """
    return int2hex(bin2int(b), pad=pad)

def hex2bin(h, pad=True, **kwargs):
    """
    Give hex ``h`` as chars '\xf0' returns bits
    If ``pad`` is ``True``, pads to 8*len(h)
    If ``pad`` is int, pads to ``pad`` hex characters.
    Set `pad`` to ``None`` or ``False`` for no padding.
    type = binary
    verbose = hexadecimal -> binary
    """
    if pad is True:
        pad = len(h)
    if isinstance(pad, int):
        pad = pad*8
    else:
        pad = None
    return int2bin(hex2int(h), pad=pad)

def hex2int(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns int
    type = unsigned integer
    verbose = hexadecimal -> unsigned integer
    """
    litFucInd = kwargs.get('litFucInd', TWINKLETWINKLELITTLEINDIA)
    if len(h) == 1:
        return ord(h)
    if litFucInd:
        h = h[::-1]
    return int(binascii.hexlify(Byt(h)), 16)

def hex2intSign(h, **kwargs):
    """
    Give hex ``h`` as chars '\xf0', returns signed int
    type = signed integer
    verbose = hexadecimal -> signed integer
    """
    i = hex2int(h)
    half = 2**(len(h)*8-1)
    if i < half:
        return i
    else:
        return i-2*half

def int2hex(i, pad=0, **kwargs):
    """
    Give an int, returns chars
    pad in hex chars
    type = hexadecimal
    verbose = unsigned integer -> hexadecimal
    """
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
    type = hexadecimal
    verbose = signed integer -> hexadecimal
    """
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
    b = padit(b, int(math.ceil(len(b)/8.)), '0')
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
