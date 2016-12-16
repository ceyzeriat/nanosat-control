#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import raises
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.ccsds import ccsdsexception as exc
from ctrl import core


def test_ccsdskey_base():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    assert p.name == "pt"
    assert p.dic != None
    assert p.fctdepack == None
    assert p.fctpack == None
    assert p.can_depack == True
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

def test_depack():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    assert p.depack('111011', raw=True) == '0'
    assert p.depack('111011') == 'aa'
    assert p.depack('111101', offset=1) == 'aa'
    p = CCSDSKey('pt', start=3, l=1, fctdepack=int)
    assert p.can_depack == True
    assert p.can_pack == False
    assert p.depack('11101') is 0
    p = CCSDSKey('pt', l=1, fctdepack=int)
    assert p.depack('01111', rel=True) is 0
    p = CCSDSKey('pt', l=1, fctpack=bool)
    assert p.depack('01111', rel=True, raw=True) == '0'
    p = CCSDSKey('pt', start=0, l=4, fctdepack=core.bin2int)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.depack('0011') == 12
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.depack('0011') == 3
    p = CCSDSKey('pt', dic={'aa': '01', 'bb': '10'}, start=0, l=2)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.depack('01') == 'bb'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.depack('01') == 'aa'


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
    assert p.pack('bb') == '10'

@raises(exc.CantApplyOffset)
def test_ccsdskey_CantApplyOffset():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    p.cut_offset(-4)

@raises(exc.BadDefinition)
def test_ccsdskey_BadDefinition1():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1, fctpack=int)

@raises(exc.BadDefinition)
def test_ccsdskey_BadDefinition2():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1, fctdepack=int)

@raises(exc.BadDefinition)
def test_ccsdskey_BadDefinition3():
    p = CCSDSKey('pt', start=3, l=1)

@raises(exc.NoDic)
def test_ccsdskey_NoDic():
    p = CCSDSKey('pt', start=3, l=1, fctpack=int)
    assert p.can_depack == False
    assert p.can_pack == True
    dum = p['hop']

@raises(exc.NoSuchValue)
def test_ccsdskey_NoSuchValue():
    p = CCSDSKey('pt', dic={'aa': '0', 'bb': '1'}, start=3, l=1)
    dum = p._dic_rev('3')

@raises(exc.NoDepack)
def test_ccsdskey_NoDepack():
    p = CCSDSKey('pt', start=3, l=1, fctpack=bool)
    dum = p.depack('01111')

@raises(exc.NoAbsGrab)
def test_ccsdskey_NoAbsGrab():
    p = CCSDSKey('pt', l=1, fctdepack=bool)
    assert p.relative_only == True
    dum = p.depack('01111')

@raises(exc.GrabFail)
def test_ccsdskey_GrabFail():
    p = CCSDSKey('pt', start=3, l=3, fctdepack=bool)
    dum = p.depack('01111')
