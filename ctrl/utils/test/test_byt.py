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
    assert Byt() == Byt('')
    assert Byt('z') != Byt('a')
    assert not Byt('z') == Byt('a')
    assert Byt('z') != 23
    assert not Byt('z') == 23
    assert Byt([0, 1, 2]) == Byt('\x00\x01\x02')
    assert Byt('abc') == Byt([97, 98, 99])
    assert Byt(b'abc') == Byt([97, 98, 99])
    assert Byt(u'abc') == Byt([97, 98, 99])

def test_slice_iter():
    assert Byt('abc')[0] == Byt('a')
    assert Byt('abc')[-1] == Byt('c')
    assert Byt('azc')[-2:-1] == Byt('z')
    assert Byt('azc')[-2:] == Byt('zc')
    assert Byt('abc')[0:1] == Byt('a')
    assert Byt('azc')[:2] == Byt('az')
    assert [ch for ch in Byt('azc')] == [Byt('a'), Byt('z'), Byt('c')]
    assert [ch for ch in Byt('')] == []
    assert [ch for ch in Byt('azc')[:2]] == [Byt('a'), Byt('z')]
    assert [ch for ch in Byt('az')[0]] == [Byt('a')]
    assert [ch for ch in Byt('abc').iterInts()] == [97, 98, 99]
    assert [ch for ch in Byt('').iterInts()] == []
    assert [ch for ch in Byt('abc')[:2].iterInts()] == [97, 98]
    assert [ch for ch in Byt('az')[0].iterInts()] == [97]
    assert [ch for ch in Byt('abc').iterInts()] == Byt('abc').ints()

def test_str_concat():
    assert str(Byt('abc')) == 'abc'
    assert repr(Byt('abc')) == "Byt('abc')"
    assert Byt('az') + Byt('a') == Byt('aza')
    assert Byt('a') + Byt('az')[0] == Byt('aa')
    assert Byt('abc').hex() == '61 62 63'
    assert Byt('abc')[0].hex() == '61'
    assert Byt('a')[-1] * 2 == Byt('aa')
    assert 2 * Byt('za')[0] == Byt('zz')
    assert Byt('a') in Byt('zaz')
    assert Byt('a') not in Byt('zcz')

def test_fct():
    assert Byt('abc').split() == [Byt('abc')]
    assert Byt('azc').split(Byt('z')) == [Byt('a'), Byt('c')]
    assert Byt('azczd').split(Byt('z'), 1) == [Byt('a'), Byt('czd')]
    assert Byt('azczd').rsplit(Byt('z'), 1) == [Byt('azc'), Byt('d')]
    assert Byt('abc').replace(Byt('a'), Byt('t')) == Byt('tbc')
    assert Byt('abc').zfill(4) == Byt('0abc')
    assert Byt('abc').zfill(2) == Byt('abc')
    assert Byt('abc').strip(Byt('a')) == Byt('bc')
    assert Byt('azc').strip(Byt('az')) == Byt('c')
    assert Byt('azc').strip(Byt('za')) == Byt('c')
    assert Byt('azc').rstrip(Byt('ac')) == Byt('az')
    assert Byt('abc').lstrip(Byt('ac')) == Byt('bc')
    assert Byt(' ').join([]) == Byt()
    assert Byt(' ').join([Byt('a'), Byt('z')]) == Byt('a z')
    assert Byt(' ').join([Byt('az')]) == Byt('az')
    assert Byt(' ').join(Byt('az')) == Byt('a z')

@raises(TypeError)
def test_wrong_eq():
    Byt('a') == 'a'

@raises(TypeError)
def test_wrong_ne():
    Byt('a') != 'c'

@raises(TypeError)
def test_wrong_concat():
    Byt('a') + 'az'

@raises(TypeError)
def test_wrong_concat2():
    'az' + Byt('a')

@raises(TypeError)
def test_contains():
    'r' in Byt('azc')

@raises(TypeError)
def test_wrong_split():
    Byt('azczd').split('z')

@raises(TypeError)
def test_wrong_rsplit():
    Byt('azczd').rsplit('z')

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
    Byt('azc').join(['a', Byt('z')])

@raises(TypeError)
def test_wrong_eq_bis():
    Byt('a') == b'a'

@raises(TypeError)
def test_wrong_ne_bis():
    Byt('a') != b'c'

@raises(TypeError)
def test_wrong_concat_bis():
    Byt('a') + b'az'

@raises(TypeError)
def test_wrong_concat2_bis():
    b'az' + Byt('a')

@raises(TypeError)
def test_contains_bis():
    b'r' in Byt('azc')

@raises(TypeError)
def test_wrong_split_bis():
    Byt('azczd').split(b'z')

@raises(TypeError)
def test_wrong_rsplit_bis():
    Byt('azczd').rsplit(b'z')

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
    Byt('azc').join([b'a', Byt('z')])

@raises(TypeError)
def test_wrong_eq_ter():
    Byt('a') == u'a'

@raises(TypeError)
def test_wrong_ne_ter():
    Byt('a') != u'c'

@raises(TypeError)
def test_contains_ter():
    u'r' in Byt('azc')
