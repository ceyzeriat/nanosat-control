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


import re
import inflect
import sys
from multiprocessing import current_process
from dateutil import parser
from byt import Byt
from sympy import solve, sympify


from .posixutc import PosixUTC
from . import PYTHON3


# make sure that python 3 understands unicode native python 2 function
if PYTHON3:
    unicode = str


def prepare_terminal(txt):
    ### os.system("reset")
    sys.stdout.write("\x1b]2;{}\x07".format(txt))


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


def strISOstamp2datetime(txt):
    """
    Tranforms a ISO date string into a datetime
    """
    return parser.parse(str(txt))


def now():
    """
    Returns the now timestamp as datetime
    """
    return PosixUTC.now()


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


CRC32TABLE = []
poly = 0xEDB88320
for byte in range(256):
    for i in range(8):
        byte = (byte >> 1) ^ (poly & (-(byte & 1)))
    CRC32TABLE.append(byte)
del poly, i, byte

def crc32(message, crc=None):
    """
    Give a message, returns a CRC on 4 octet using
    basecrc as crc start-value (if given)
    """
    crc = 0xffffffff if crc is None else int(crc)
    for byte in Byt(message).iterInts():
        crc = (crc >> 8) ^ CRC32TABLE[(crc ^ byte) & 0xFF]
    return two_comp_uint(crc, 32)



# lookup table for cimputing payload crc
payload_crc_table = {}
poly = 0x04C11DB7
for byte in range(256):
    c = byte << 24
    for i in range(8):
        c = (c << 1) ^ poly if (c & 0x80000000) else c << 1
    payload_crc_table[byte] = c & 0xffffffff
del poly, i, byte, c

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

