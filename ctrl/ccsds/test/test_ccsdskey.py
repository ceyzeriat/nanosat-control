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
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.ccsds import ccsdsexception
from ctrl.utils import core


def test_ccsdskey_base():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    assert p.name == "pt"
    assert p.dic != None
    assert p._fctunpack == None
    assert p._fctpack == None
    assert p.can_unpack == True
    assert p.can_pack == True
    assert p.relative_only == False
    assert p.len == 1
    assert p.start == 3
    assert p.cut_offset(1) == slice(4, 5)
    assert p.cut_offset(-1) == slice(2, 3)
    assert p._dic_rev('0') == 'aa'
    assert p._dic_rev(1) == 'bb'
    p = CCSDSKey('pt', dic={'aa': 0, 'bb': 1}, start=3, l=1)
    assert p._dic_rev('0') == 'aa'
    assert p._dic_rev(1) == 'bb'

def test_unpack():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    assert p.unpack('111011', raw=True) == '0'
    assert p.unpack('111011') == 'aa'
    assert p.unpack('111101', offset=1) == 'aa'
    p = CCSDSKey('pt', start=3, l=1, fctunpack=int)
    assert p.can_unpack == True
    assert p.can_pack == False
    assert p.unpack('11101') is 0
    p = CCSDSKey('pt', l=1, fctunpack=int)
    assert p.unpack('0', rel=True) is 0
    p = CCSDSKey('pt', l=1, fctpack=bool)
    assert p.unpack('0', rel=True, raw=True) == '0'
    p = CCSDSKey('pt', start=0, l=4, fctunpack=core.bin2int)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.unpack('0011') == 12
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.unpack('0011') == 3
    p = CCSDSKey('pt', dic={'aa': '01', 'bb': '10'}, start=0, l=2)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.unpack('01') == 'bb'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.unpack('01') == 'aa'


def test_pack():
    p = CCSDSKey('pt', dic={'aa': '01', 'bb': '10'}, start=3, l=1)
    assert p.can_pack == True
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.pack('aa') == '10'
    assert p.pack('bb') == '01'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.pack('aa') == '01'
    assert p.pack('bb') == '10'
    p = CCSDSKey('pt', start=3, l=2, fctpack=core.int2bin)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.pack(1, raw=True) == '10'
    assert p.pack(1, raw=True, pad=3) == '100'
    assert p.pack(3, pad=3) == '110'
    assert p.pack(1) == '10'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.pack(1, raw=True) == '01'
    assert p.pack(1, raw=True, pad=3) == '001'
    assert p.pack(3, pad=3) == '011'
    assert p.pack(1) == '01'
    p = CCSDSKey('pt', dic={'aa': '01', 'bb': '10'}, start=0, l=2, dic_force='aa')
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.pack('aa') == '10'
    assert p.pack('bb') == '10'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.pack('aa') == '01'
    assert p.pack('bb') == '01'

@raises(ccsdsexception.CantApplyOffset)
def test_ccsdskey_CantApplyOffset():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    p.cut_offset(-4)

@raises(ccsdsexception.BadDefinition)
def test_ccsdskey_BadDefinition1():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1, fctpack=int)

@raises(ccsdsexception.BadDefinition)
def test_ccsdskey_BadDefinition2():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1, fctunpack=int)

@raises(ccsdsexception.BadDefinition)
def test_ccsdskey_BadDefinition3():
    p = CCSDSKey('pt', start=3, l=1)

@raises(ccsdsexception.NoDic)
def test_ccsdskey_NoDic():
    p = CCSDSKey('pt', start=3, l=1, fctpack=int)
    assert p.can_unpack == False
    assert p.can_pack == True
    dum = p['hop']

@raises(ccsdsexception.NoSuchValue)
def test_ccsdskey_NoSuchValue():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    dum = p._dic_rev('3')

@raises(ccsdsexception.NoUnpack)
def test_ccsdskey_NoUnpack():
    p = CCSDSKey('pt', start=3, l=1, fctpack=bool)
    dum = p.unpack('01111')

@raises(ccsdsexception.NoAbsGrab)
def test_ccsdskey_NoAbsGrab():
    p = CCSDSKey('pt', l=1, fctunpack=bool)
    assert p.relative_only == True
    dum = p.unpack('01111')

@raises(ccsdsexception.GrabFail)
def test_ccsdskey_GrabFail():
    p = CCSDSKey('pt', start=3, l=3, fctunpack=bool)
    dum = p.unpack('01111')
