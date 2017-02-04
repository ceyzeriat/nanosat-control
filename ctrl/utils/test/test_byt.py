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
from ctrl.utils import Byt


def test_creation():
    assert Byt() == b''
    assert Byt() == Byt('')
    assert Byt([0, 1, 2]) == Byt('\x00\x01\x02')
    assert Byt('abc') == Byt([97, 98, 99])
    assert Byt(b'abc') == Byt([97, 98, 99])
    assert Byt(u'abc') == Byt([97, 98, 99])

def test_slice_iter():
    assert Byt('abc')[0] == Byt('a')
    assert Byt('abc')[0] == b'a'
    assert Byt('abc')[0:1] == Byt('a')
    assert Byt('abc')[0:2] == Byt('ab')
    assert [ch for ch in Byt('abc')] == [Byt('a'), Byt('b'), Byt('c')]
    assert [ch for ch in Byt('')] == []
    assert [ch for ch in Byt('abc')[:2]] == [Byt('a'), Byt('b')]
    assert [ch for ch in Byt('ab')[0]] == [Byt('a')]
    assert [ch for ch in Byt('abc').iterInts()] == [97, 98, 99]
    assert [ch for ch in Byt('').iterInts()] == []
    assert [ch for ch in Byt('abc')[:2].iterInts()] == [97, 98]
    assert [ch for ch in Byt('ab')[0].iterInts()] == [97]
    assert [ch for ch in Byt('abc').iterInts()] == Byt('abc').ints()

def test_str_concat():
    assert str(Byt('abc')) == 'abc'
    assert repr(Byt('abc')) == "Byt('abc')"
    assert Byt('ab') + Byt('a') == Byt('aba')
    assert Byt('a') + Byt('ab')[0] == Byt('aa')
    assert Byt('abc').hex() == '61 62 63'
    assert Byt('abc')[0].hex() == '61'

def test_fct():
    assert Byt('abc').split() == [Byt('abc')]
    assert Byt('abc').split(Byt('b')) == [Byt('a'), Byt('c')]
    assert Byt('abcbd').split(Byt('b'), 1) == [Byt('a'), Byt('cbd')]
    assert Byt('abcbd').rsplit(Byt('b'), 1) == [Byt('abc'), Byt('d')]
    assert Byt('abc').replace(Byt('a'), Byt('t')) == Byt('tbc')
    assert Byt('abc').zfill(4) == Byt('0abc')
    assert Byt('abc').zfill(2) == Byt('abc')
    assert Byt('abc').strip(Byt('a')) == Byt('bc')
    assert Byt('abc').strip(Byt('ab')) == Byt('c')
    assert Byt('abc').rstrip(Byt('ac')) == Byt('ab')
    assert Byt('abc').lstrip(Byt('ac')) == Byt('bc')
    assert Byt(' ').join([]) == Byt()
    assert Byt(' ').join([Byt('a'), Byt('b')]) == Byt('a b')
    assert Byt(' ').join([Byt('ab')]) == Byt('ab')
    assert Byt(' ').join(Byt('ab')) == Byt('a b')

@raises(TypeError)
def test_wrong_concat():
    Byt('a') + 'ab'

@raises(TypeError)
def test_wrong_concat2():
    'ab' + Byt('a')

@raises(TypeError)
def test_wrong_split():
    Byt('abcbd').split('b')

@raises(TypeError)
def test_wrong_rsplit():
    Byt('abcbd').rsplit('b')

@raises(TypeError)
def test_wrong_replace():
    Byt('abc').replace('a', Byt('t'))

@raises(TypeError)
def test_wrong_replace2():
    Byt('abc').replace(Byt('a'), 't')

@raises(TypeError)
def test_wrong_strip():
    Byt('abc').strip('a')

@raises(TypeError)
def test_wrong_lstrip():
    Byt('abc').lstrip('a')

@raises(TypeError)
def test_wrong_rstrip():
    Byt('abc').rstrip('a')

@raises(TypeError)
def test_wrong_join():
    Byt('abc').join(['a', Byt('b')])

@raises(TypeError)
def test_wrong_concat_bis():
    Byt('a') + b'ab'

@raises(TypeError)
def test_wrong_concat2_bis():
    b'ab' + Byt('a')

@raises(TypeError)
def test_wrong_split_bis():
    Byt('abcbd').split(b'b')

@raises(TypeError)
def test_wrong_rsplit_bis():
    Byt('abcbd').rsplit(b'b')

@raises(TypeError)
def test_wrong_replace_bis():
    Byt('abc').replace(b'a', Byt('t'))

@raises(TypeError)
def test_wrong_replace2_bis():
    Byt('abc').replace(Byt('a'), b't')

@raises(TypeError)
def test_wrong_strip_bis():
    Byt('abc').strip(b'a')

@raises(TypeError)
def test_wrong_lstrip_bis():
    Byt('abc').lstrip(b'a')

@raises(TypeError)
def test_wrong_rstrip_bis():
    Byt('abc').rstrip(b'a')

@raises(TypeError)
def test_wrong_join_bis():
    Byt('abc').join([b'a', Byt('b')])
