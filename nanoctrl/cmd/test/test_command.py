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


from byt import Byt
from nose.tools import raises
from nanoctrl.cmd.cm import Cm
from nanoctrl.cmd import cmdexception
import copy
from param.param_commands import RANGESEPARATOR


def ftup(x, y):
    return "{}{}{}".format(x, RANGESEPARATOR, y)


echo = {'number':1,
        'name': 'echo',
        'subsystem': 'obc',
        'pid': "L0ComManager",
        'desc': "blah",
        'lparam': 2,
        'param': (('hop', 'blah', ftup(0, 255), 'str', 2), )}

echo2 = {'number':1,
        'name': 'echo',
        'subsystem': 'obc',
        'pid': "L0ComManager",
        'desc': "blah",
        'lparam': 2,
        'param': (('hop', 'blah', ftup(0, 255), 'str', ftup(1,2)), )}

echo3 = {'number':1,
        'name': 'echo',
        'subsystem': 'obc',
        'pid': "L0ComManager",
        'desc': "blah",
        'lparam': "*",
        'param': (('hop', 'blah', ftup(0, 255), 'str', ftup(1,2)), )}


def test_cm_base():
    c = Cm(**echo)
    assert c.number == 1
    assert c.name == 'echo'
    assert c.desc == 'blah'
    assert c.level == 0
    assert c.subsystem == "obc"
    assert c.pid == "L0ComManager"
    assert c.lparam == 2
    assert c.nparam == 1
    assert c.p_0_hop.typ.typ == 'str'

def test_cm_base2():
    ee = copy.deepcopy(echo)
    ee['lparam'] = '*'
    ee['param'] = (('hop', 'blah', ftup(0, 255), 'str', ftup(1, 4)), )
    c = Cm(**ee)
    assert c.number == 1
    assert c.name == 'echo'
    assert c.desc == 'blah'
    assert c.level == 0
    assert c.subsystem == "obc"
    assert c.pid == "L0ComManager"
    assert c.lparam is None
    assert c.nparam == 1
    assert c.p_0_hop.typ.typ == 'str'
    assert c.generate_data(hop='abab')[0] == Byt('\x61\x62\x61\x62')
    assert c.generate_data(hop='a')[0] == Byt('\x61')

def test_cm_call():
    c = Cm(**echo)
    assert c.generate_data(hop='ab')[0] == Byt('\x61\x62')
    assert c.generate_data(hop='ab')[1] == {'hop': 'ab'}
    assert c(hop='ab') == c.generate_data(hop='ab')

@raises(cmdexception.WrongPID)
def test_cm_WrongPID():
    ee = copy.deepcopy(echo)
    ee['pid'] = 'tadaaaam'
    c = Cm(**ee)

@raises(cmdexception.WrongParameterDefinition)
def test_cm_WrongParameterDefinition():
    ee = copy.deepcopy(echo)
    ee['param'] = (('hop', 'blah'), )
    c = Cm(**ee)

@raises(cmdexception.MissingCommandInput)
def test_cm_MissingCommandInput():
    c = Cm(**echo)
    c.generate_data('\x00')

@raises(cmdexception.WrongCommandLength)
def test_cm_WrongCommandLength():
    c = Cm(**echo2)
    c.generate_data(hop='a')

@raises(cmdexception.InvalidParameterValue)
def test_cm_InvalidParameterValue():
    c = Cm(**echo3)
    c.generate_data(hop='abc')
