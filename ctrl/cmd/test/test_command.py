#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import raises
from ctrl.cmd.cm import Cm
from ctrl.cmd import cmdexception
import copy
from ctrl.cmd.param_commands import RANGESEPARATOR

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

def test_cm_call():
    c = Cm(**echo)
    assert c.generate_data(hop='ab')[0] == '\x61\x62'
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

@raises(cmdexception.MissingCmInput)
def test_cm_MissingCmInput():
    c = Cm(**echo)
    c.generate_data('\x00')

@raises(cmdexception.WrongCmLength)
def test_cm_WrongCmLength():
    c = Cm(**echo2)
    c.generate_data(hop='a')
