#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import cmdexception as exc
from .. import core
from .pformat import PFormat


__all__ = ['Param']


class Parameter(object):
    def __init__(self, name, desc, rng, typ=None, size=1, unit=None):
        """
        Creates a self-checking parameter used in a command

        Args:
        * name (str): the name of the parameter.
          Use characters: a-z, A-Z, 0-9 and _ only.
        * desc (str): the description of the parameter
        * rng (min-max tuple, list or dict): if min-max tuple: the
          min and max values the parameter should take (bounds inclusive),
          if list: the allowed values,
          if dict: the allowed keys; in that case, ``typ`` is irrelevant.
        * typ (Format or str): the type of the parameter, alternatively, a
          string defining it, e.g. ``int8``, ``float32``, ``str``, ``unit16``.
        * size (int): the maximum length of the expected input,
          which is padded with 0 if smaller
        * unit (str or None): the unit of the parameter
        """
        self._name = core.clean_name(name)
        self._desc = str(desc)
        self._unit = str(unit) if unit is not None else ""
        self._isdict = isinstance(rng, dict)
        if self._isdict:
            self._typ = "<dict>"
            self._rng = rng
            self._rngdisp = repr(self.rng.keys())
        else:
            self._typ = PFormat(typ)
            if isinstance(rng, tuple):
                self._rng = (rng[0], rng[1])
                if self.typ.typ != 'str':
                    if not (self.typ.is_valid(self.rng[0])
                            and self.typ.is_valid(self.rng[1])):
                        raise exc.WrongParameterDefinition(self.name, 'rng')
                else:
                    if not (isinstance(self.rng[0], int)
                            and isinstance(self.rng[1], int)):
                        raise exc.WrongParameterDefinition(self.name, 'rng')
                self._rngdisp = "[{}--{}]".format(*self.rng)
            elif hasattr(rng, "__iter__"):
                self._rng = list(rng)
                for item in self.rng:
                    if self.typ.typ != 'str':
                        if not self.typ.is_valid(item):
                            raise exc.WrongParameterDefinition(self.name,'rng')
                    else:
                        if not isinstance(item, int):
                            raise exc.WrongParameterDefinition(self.name,'rng')
                self._rngdisp = repr(self.rng)
            else:
                raise exc.WrongParameterDefinition(self.name, 'rng')
        if not isinstance(size, int) or size <= 0:
            raise exc.WrongParameterDefinition(self.name, 'size')
        self._size = int(size)

    def __str__(self):        
        return " {}{} {}[{}]: {}\n  {}".format(
                        self.name,
                        " ({})".format(self.unit) if self.unit != "" else "",
                        self.typ,
                        self.size,
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
            if len(value) != self.size:
                return False
            for item in value:
                if not item in self.rng.keys():
                    return False
            if withvalue:
                return True, value
            else:
                return True
        if not hasattr(value, "__iter__"):
            # split input string into ['a', 'b', ...]
            if self.typ.typ == 'str':
                if not isinstance(value, str):
                    return False
                value = [item for item in value]
            else:
                value = [value]
        if len(value) != self.size:
            return False
        # checks ranges and types
        for item in value:
            # checks types
            if not self.typ.is_valid(item):
                return False
            if self.typ.typ == 'str':
                item = ord(item)
            # checks ranges
            if isinstance(self.rng, list):
                if not item in self.rng:
                    return False
            elif isinstance(self.rng, tuple):
                if not self.rng[0] <= item <= self.rng[1]:
                    return False
            else:
                return False
        if withvalue:
            return True, value
        else:
            return True

    def tohex(self, value):
        """
        Equivalent of calling the object
        """
        rep = self.is_valid(value, withvalue=True)
        if rep is False:
            raise exc.InvalidParameterValue(self.name, value)
        else:
            valid, value = rep
        ret = ""
        if self._isdict:
            for item in value:
                ret += self.rng[item]
        else:
            for item in value:
                ret += self.typ._tohex(item)
        return ret

    @property
    def man(self):
        return str(self)

    @man.setter
    def man(self, value):
        raise exc.ReadOnly('man')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise exc.ReadOnly('name')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        raise exc.ReadOnly('desc')    

    @property
    def typ(self):
        return self._typ

    @typ.setter
    def typ(self, value):
        raise exc.ReadOnly('typ')

    @property
    def rng(self):
        return self._rng

    @rng.setter
    def rng(self, value):
        raise exc.ReadOnly('rng')

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        raise exc.ReadOnly('size')

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        raise exc.ReadOnly('unit')
