#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import raises
from ctrl.command import Command
from ctrl import cmdexception as exc
import copy


echo = {'number':1,
        'name': 'echo',
        'level': 0,
        'subsystem': '',
        'apid':  34,
        'desc': "blah",
        'lparam': 2,
        'param': (('hop', 'blah', (0, 255), 'str', 2), ),
        'nparam': 1}


def test_command_base():
    c = Command(**echo)
    assert c.number == 1
    assert c.name == 'echo'
    assert c.desc == 'blah'
    assert c.level == 0
    assert c.subsystem == ""
    assert c.apid == 34
    assert c.lparam == 2
    assert c.p_0_hop.typ.typ == 'str'

def test_command_call():
    c = Command(**echo)
    assert c.call(hop='ab') == '\x61\x62'
    assert c(hop='ab') == '\x61\x62'

@raises(exc.WrongParamCount)
def test_command_WrongParamCount():
    ee = copy.deepcopy(echo)
    ee['nparam'] = 2
    c = Command(**ee)

@raises(exc.WrongParameterDefinition)
def test_command_WrongParameterDefinition():
    ee = copy.deepcopy(echo)
    ee['param'] = (('hop', 'blah'), )
    c = Command(**ee)

@raises(exc.MissingCommandInput)
def test_command_MissingCommandInput():
    c = Command(**echo)
    c.call('\x00')
