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
from param import param_commands
from . import cmdexception
from ..utils import core
from .pformat import PFormat


__all__ = ['Param']


class Parameter(object):
    def __init__(self, name, desc, rng, typ=None, size=1, unit=None, exval=None):
        """
        Creates a self-checking parameter used in a command

        Args:
        * name (str): the name of the parameter.
          Use characters: a-z, A-Z, 0-9 and _ only.
        * desc (str): the description of the parameter
        * rng (min-max str, list or dict): if 'min-max' str: the
          min and max values the parameter should take (bounds inclusive),
          if list: the allowed values,
          if dict: the allowed keys; in that case, ``typ`` is irrelevant.
        * typ (Format or str): the type of the parameter, alternatively, a
          string defining it, e.g. ``int8``, ``float32``, ``str``, ``unit16``.
        * size (min-max str or int): the min and max acceptable length of the
          expected input (bounds inclusive), or if 'int' the exact length
        * unit (str or None): the unit of the parameter
        * exval (srt): an example value for the parameter
        """
        self._name = core.clean_name(name)[:param_commands.LENPARAMNAME]
        self._desc = str(desc)
        self._unit = str(unit) if unit is not None else ""
        self._isdict = isinstance(rng, dict)
        if exval is None or len(str(exval)) == 0:
            self.exval = None
        else:
            self.exval = repr(exval)
        if self._isdict:
            self._typ = "<dict>"
            self._rng = rng
            self._rngdisp = repr(self.rng.keys())
        else:
            self._typ = PFormat(typ)
            if rng == "" or rng == "*":  # just force default range
                rng = "{}{}{}".format(self.typ.minmax[0],
                                      param_commands.RANGESEPARATOR,
                                      self.typ.minmax[1])
            elif rng.find(param_commands.LISTSEPARATOR) != -1:  # we got a list
                rng = [item.strip()
                        for item in rng.split(param_commands.LISTSEPARATOR)]
            # if we have a min-max range
            if core.isStr(rng):
                self._rng = rng.split(param_commands.RANGESEPARATOR)[:2]
                self._rng = tuple([core.to_num(item) for item in self._rng])
                if self.typ.typ != 'str':
                    if not (self.typ.is_valid(self.rng[0])
                            and self.typ.is_valid(self.rng[1])):
                        raise cmdexception.WrongParameterDefinition(self.name,
                                                                    'rng')
                else:
                    if not (isinstance(self.rng[0], int)
                            and isinstance(self.rng[1], int)):
                        raise cmdexception.WrongParameterDefinition(self.name,
                                                                    'rng')
                self._rngdisp = "[{}--{}]".format(*self.rng)
            elif hasattr(rng, "__iter__"):
                self._rng = list(map(core.to_num, rng))
                for item in self.rng:
                    if self.typ.typ != 'str':
                        if not self.typ.is_valid(item):
                            raise cmdexception.WrongParameterDefinition(
                                                                self.name,
                                                                'rng')
                    else:
                        if not isinstance(item, int):
                            raise cmdexception.WrongParameterDefinition(
                                                                self.name,
                                                                'rng')
                self._rngdisp = repr(self.rng)
            else:
                raise cmdexception.WrongParameterDefinition(self.name, 'rng')
        if core.isStr(size) and str(size) == '*':
            self._sizedisp = '[*]'
            self._size = None
        elif core.isStr(size) and not str(size).isdigit():
            self._size = size.split(param_commands.RANGESEPARATOR)[:2]
            self._size = tuple([core.to_num(item) for item in self._size])
            self._sizedisp = "[{}--{}]".format(*self.size)
            if not isinstance(self.size[0], int) \
                    or not isinstance(self.size[1], int):
                raise cmdexception.WrongParameterDefinition(self.name, 'size')
            if self.size[0] < 0 or self.size[1] < 0 \
                    or self.size[0] > self.size[1]:
                raise cmdexception.WrongParameterDefinition(self.name, 'size')
        elif (isinstance(size, int) and size > 0) or str(size).isdigit():
            self._size = int(size)
            self._sizedisp = "[{}]".format(self.size)
        else:
            raise cmdexception.WrongParameterDefinition(self.name, 'size')

    def __str__(self):        
        return " {}{} {}{}: {}\n  {}".format(
                        self.name,
                        " ({})".format(self.unit) if self.unit != "" else "",
                        self.typ,
                        self._sizedisp,
                        self._rngdisp,
                        self.desc)

    __repr__ = __str__

    def __call__(self, value):
        return self.tohex(value)

    def is_valid(self, value, withvalue=False):
        """
        Checks the validity of the ranges and the types of the given
        value(s).
        Returns ``False`` is any of the value is not compliant.

        Args:
        * value: the value or the list of values to check
        """
        if self._isdict:
            if not hasattr(value, "__iter__"):
                value = [value]
            if isinstance(self.size, int) and len(value) != self.size:
                return (False, value) if withvalue else False
            elif isinstance(self.size, tuple) and \
                    (len(value) < self.size[0] or len(value) > self.size[1]):
                return (False, value) if withvalue else False
            # if None, no size to check
            elif self.size is not None:
                return (False, value) if withvalue else False
            for item in value:
                if not item in self.rng.keys():
                    return (False, value) if withvalue else False
            return (True, value) if withvalue else True
        if not hasattr(value, "__iter__") or core.isStr(value):
            # split input string into ['a', 'b', ...]
            if self.typ.typ == 'str':
                if not core.isStr(value):
                    return (False, value) if withvalue else False
                value = [item for item in value]
            else:
                value = [value]
        if isinstance(self.size, tuple):
            if len(value) < self.size[0] or len(value) > self.size[1]:
                return (False, value) if withvalue else False
        elif isinstance(self.size, int):
            if len(value) != self.size:
                return (False, value) if withvalue else False
        # if None, no size to check
        elif self.size is not None:
            return (False, value) if withvalue else False
        # checks ranges and types
        for item in value:
            # checks types
            if not self.typ.is_valid(item):
                return (False, value) if withvalue else False
            if self.typ.typ == 'str':
                item = ord(item)
            # checks ranges
            if isinstance(self.rng, list):
                if not item in self.rng:
                    return (False, value) if withvalue else False
            elif isinstance(self.rng, tuple):
                if not self.rng[0] <= item <= self.rng[1]:
                    return (False, value) if withvalue else False
            else:
                return (False, value) if withvalue else False
        return (True, value) if withvalue else True

    def tohex(self, value):
        """
        Equivalent of calling the object
        """
        valid, value = self.is_valid(value, withvalue=True)
        if valid is False:
            raise cmdexception.InvalidParameterValue(self.name, value)
        ret = Byt()
        if self._isdict:
            for item in value:
                ret += Byt(self.rng[item])
        else:
            for item in value:
                ret += self.typ._tohex(item)
        return ret

    @property
    def man(self):
        return str(self)

    @man.setter
    def man(self, value):
        raise cmdexception.ReadOnly('man')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise cmdexception.ReadOnly('name')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        raise cmdexception.ReadOnly('desc')    

    @property
    def typ(self):
        return self._typ

    @typ.setter
    def typ(self, value):
        raise cmdexception.ReadOnly('typ')

    @property
    def rng(self):
        return self._rng

    @rng.setter
    def rng(self, value):
        raise cmdexception.ReadOnly('rng')

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        raise cmdexception.ReadOnly('size')

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        raise cmdexception.ReadOnly('unit')
