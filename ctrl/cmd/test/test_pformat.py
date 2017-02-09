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


from nose.tools import raises
from ctrl.cmd.pformat import PFormat
from ctrl.cmd import cmdexception
from ctrl.utils import Byt


def test_pformat_parse():
    p = PFormat('str')
    assert p._parse('zertzrt') is None
    assert p._parse('int') is None
    assert p._parse('float') is None
    assert p._parse('uint') is None
    assert p._parse('str') == ('str', 0)
    assert p._parse('int8') == ('int', 8)
    assert p._parse('<uint-16>') == ('uint', 16)
    assert p._parse('<float(32)>') == ('float', 32)

def test_pformat_str():
    p = PFormat('str')
    assert p.minmax == (0, 255)
    assert p.bits == 0
    assert p.typ == 'str'
    assert p.is_valid(['a']) == False
    assert p.is_valid('ab') == False
    assert p.is_valid(32) == False
    assert p.is_valid('a') == True
    assert p.is_valid('\x01') == True
    assert p._tohex('a') == Byt('a')
    assert p._tohex('\x41') == Byt('A')

def test_pformat_nostr():
    p = PFormat('int', 8)
    assert p.minmax == (-2**7, 2**7-1)
    assert p.bits == 8
    assert p.typ == 'int'
    assert p._halfmaxint == 2**7
    assert p._maxint == 2**8

def test_pformat_int():
    p = PFormat('int', 8)
    assert p.is_valid(128) == False
    assert p.is_valid(127) == True
    assert p.is_valid(-128) == True
    assert p.is_valid(-129) == False

def test_pformat_uint():
    p = PFormat('uint', 8)
    assert p.minmax == (0, 2**8-1)
    assert p.is_valid(256) == False
    assert p.is_valid(255) == True
    assert p.is_valid(0) == True
    assert p.is_valid(-1) == False
    assert p._tohex(0) == Byt('\x00')
    assert p._tohex(241) == Byt('\xf1')

def test_pformat_float():
    p = PFormat('float', 8)
    assert p.is_valid('e') == False
    assert p.is_valid(0) == False
    assert p.is_valid(0.0) == True

@raises(cmdexception.NotImplemented)
def test_pformat_NotImplemented():
    p = PFormat('float', 8)
    p._tohex(12.0)

@raises(cmdexception.MissingFormatInput)
def test_pformat_MissingFormatInput():
    p = PFormat('int')

@raises(cmdexception.UnknownFormat)
def test_pformat_UnknownFormat():
    p = PFormat('issdgnt')

@raises(cmdexception.UnknownFormat)
def test_pformat_UnknownFormat():
    p = PFormat('issdgnt')

@raises(cmdexception.WrongFormatBitLength)
def test_pformat_WrongFormatBitLength1():
    p = PFormat('int', 0)

@raises(cmdexception.WrongFormatBitLength)
def test_pformat_WrongFormatBitLength2():
    p = PFormat('int', 8.0)

@raises(cmdexception.WrongFormatBitLength)
def test_pformat_WrongFormatBitLength3():
    p = PFormat('int', 3)

@raises(cmdexception.WrongFormatBitLength)
def test_pformat_WrongFormatBitLength4():
    p = PFormat('int', 65)
