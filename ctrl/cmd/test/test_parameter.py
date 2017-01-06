#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import raises
from ctrl.cmd.parameter import Parameter
from ctrl.cmd import cmdexception
from ctrl.cmd.param_commands import RANGESEPARATOR
from ctrl.utils import core

def ftup(x, y):
    return "{}{}{}".format(x, RANGESEPARATOR, y)


def test_param_base():
    p = Parameter('hop', 'blah', ftup(0,10), 'uint8', 3, None)
    assert p.name == 'hop'
    assert p.desc == 'blah'
    assert p.unit == ''
    assert p._isdict == False
    assert p.typ.typ == 'uint'
    assert p.typ.bits == 8
    assert p.rng == (0, 10)
    assert p.size == 3

def test_param_str_tuple():
    p = Parameter('hop', 'blah', ftup(0,10), 'str')
    assert p.is_valid('rt') == False
    assert p.is_valid(3) == False
    assert p.is_valid([10]) == False
    assert p.is_valid(['\x00']) == True
    assert p.is_valid('\x09') == True
    assert p.is_valid(['\x10']) == False
    assert p.is_valid('\x00\x00') == False
    assert p.is_valid(['\x10'], withvalue=True)[0] == False
    assert p.is_valid(['\x04'], withvalue=True) == (True, ['\x04'])
    assert p.tohex('\x04') == '\x04'
    assert p.tohex(['\x02']) == '\x02'

def test_param_str_list():
    p = Parameter('hop', 'blah', [0, 1, 2, 4], 'str', 2)
    assert p._isdict == False
    assert p.is_valid(['\x01', '\x04']) == True
    assert p.is_valid(['\x01', '\x03']) == False
    assert p.is_valid(['\x02']) == False
    assert p.is_valid(['\x00', '\x01'], withvalue=True) == (True, ['\x00', '\x01'])
    assert p.is_valid(['\x05', '\x02']) == False
    assert p.is_valid(['\x01', '\x02', '\x00']) == False
    assert p.is_valid(['\x03', '\x01'], withvalue=True)[0] == False
    assert p.is_valid('\x04\x00', withvalue=True) == (True, ['\x04', '\x00'])
    assert p.tohex(['\x04', '\x01']) == '\x04\x01'
    assert p.tohex('\x01\x02') == '\x01\x02'

def test_param_uint_tuple():
    p = Parameter('hop', 'blah', ftup(0,10), 'uint8', 1, None)
    assert p.is_valid('rt') == False
    assert p.is_valid(3) == True
    assert p.is_valid([10]) == True
    assert p.is_valid([5, 0]) == False
    assert p.is_valid([-1]) == False
    assert p.is_valid(11) == False
    assert p.is_valid([1.0]) == False
    assert p.is_valid([12.0], withvalue=True)[0] == False
    assert p.is_valid([0], withvalue=True) == (True, [0])
    assert p.tohex(3) == '\x03'
    assert p.tohex(10) == '\x0A'

def test_param_uint_list():
    p = Parameter('hop', 'blah', [0, 1, 2, 4], 'uint8', ftup(2,3), None)
    assert p._isdict == False
    assert p.is_valid('rt') == False
    assert p.is_valid(1) == False
    assert p.is_valid([2]) == False
    assert p.is_valid([0, 1], withvalue=True) == (True, [0, 1])
    assert p.is_valid([4, 2]) == True
    assert p.is_valid([1.0, 2]) == False
    assert p.is_valid([1, 2, 0]) == True
    assert p.is_valid([1, 2, 0, 0]) == False
    assert p.is_valid([0, 3]) == False
    assert p.is_valid([2.0, 1], withvalue=True)[0] == False
    assert p.is_valid([4, 0], withvalue=True) == (True, [4, 0])
    assert p.tohex([4, 1]) == '\x04\x01'
    assert p.tohex([1, 0]) == '\x01\x00'

def test_param_list():
    p = Parameter('hop', 'blah', ftup(0,65535), 'uint16', 2, None)
    core.TWINKLETWINKLELITTLEINDIA = True
    assert p.tohex([4, 260]) == '\x04\x00\x04\x01'
    core.TWINKLETWINKLELITTLEINDIA = False
    assert p.tohex([4, 260]) == '\x00\x04\x01\x04'

def test_param_dict():
    p = Parameter('hop', 'blah', {'a': '\x10', 'b': '\x45'}, size=2)
    assert p._isdict == True
    assert p.is_valid('a') == False
    assert p.is_valid(['a', 'a']) == True
    assert p.is_valid(['a', 'b']) == True
    assert p.is_valid(['a', 'c']) == False
    assert p.is_valid(['a', 'a', 'c']) == False
    assert p.is_valid(['b']) == False
    assert p.tohex(['a', 'b']) == '\x10\x45'

def test_param_dict_flexsize():
    p = Parameter('hop', 'blah', {'a': '\x10', 'b': '\x45'}, size=ftup(2,3))
    assert p._isdict == True
    assert p.is_valid('a') == False
    assert p.is_valid(['a', 'a']) == True
    assert p.is_valid(['a', 'b']) == True
    assert p.is_valid(['a', 'c']) == False
    assert p.is_valid(['a', 'b', 'a']) == True
    assert p.is_valid(['a', 'a', 'c']) == False
    assert p.is_valid(['a', 'a', 'b', 'c']) == False
    assert p.is_valid(['a', 'a', 'b', 'a']) == False
    assert p.is_valid(['b']) == False
    assert p.tohex(['a', 'b']) == '\x10\x45'

@raises(cmdexception.UnknownFormat)
def test_command_UnknownFormat():
    p = Parameter('hop', 'blah', ftup(0,255))

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition1():
    p = Parameter('hop', 'blah', [0.0, 1, 2, 4], 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition2():
    p = Parameter('hop', 'blah', [-1, 1, 2, 4], 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition3():
    p = Parameter('hop', 'blah', [0, 1, 2, 256], 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition4():
    p = Parameter('hop', 'blah', str, 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition5():
    p = Parameter('hop', 'blah', ftup(0.0, 12), 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition6():
    p = Parameter('hop', 'blah', ftup(-1, 12), 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition7():
    p = Parameter('hop', 'blah', ftup(0, 256), 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition8():
    p = Parameter('hop', 'blah', ftup('a', 256), 'uint8', 2, None)

@raises(cmdexception.WrongParameterDefinition)
def test_param_WrongParameterDefinition9():
    p = Parameter('hop', 'blah', ftup('a', 256), 'str', 2, None)

@raises(cmdexception.InvalidParameterValue)
def test_param_InvalidParameterValue():
    p = Parameter('hop', 'blah', ftup(0, 255), 'uint8', 2, None)
    assert p.is_valid(-1) == False
    p.tohex(-1)

@raises(cmdexception.InvalidParameterValue)
def test_param_InvalidParameterValue():
    p = Parameter('hop', 'blah', ftup(0, 255), 'uint8', 2, None)
    assert p.is_valid(-1) == False
    p.tohex(4.5)
