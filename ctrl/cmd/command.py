#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import cmdexception as exc
from .. import core
from . import param_commands
from .parameter import Parameter


__all__ = ['Command']


class Command(object):
    def __init__(self, number, name, apid, desc, lparam, level, subsystem, param, nparam):
        """
        Creates a self-checking command
        
        Args:
        * number (int): the unique id
        * name (str): the name (code friendly)
        * apid (int): the unique apid
        * desc (str): the description
        * lparam (int): the total length of the parameters, in octets
        * level (int): either ``0``, or ``1``, for L0 or L1
        * subsystem (str): the subsystem key
        * param (iterable of tuples): an iterable of parameter tuples of
          form and order: (name, desc, rng, typ, size, unit)
        * nparam (int): the number of parameters
        """
        if int(nparam) != len(param):
            raise exc.WrongParamCount(name, nparam)
        self._name = core.clean_name(name)
        self._number = int(number)
        self._apid = int(apid)
        self._desc = str(desc)
        self._lparam = int(lparam)
        self._subsystem = str(subsystem)
        self._param = [tuple(item) for item in param]
        self._level = 0 if str(level) == '0' else 1
        self._params = []
        for idx, item in enumerate(self._param):
            if len(item) < param_commands.MINLENPARAMSTRUCTURE:
                raise exc.WrongParameterDefinition(self.name, item[0])
            p = Parameter(*item)
            self._params.append(p)
            setattr(self, "p_{}_{}".format(idx, p.name), self._params[-1])

    def __str__(self):
        return "#{} {} (L{})\n {}\n{} params: ({} octet)\n{}".format(
                            self.number,
                            self.name,
                            int(self.level),
                            self.desc,
                            self.nparam,
                            self.lparam,
                            "\n".join([str(item) for item in self._params]))

    __repr__ = __str__

    def __call__(self, *args, **kwargs):
        return self.call(**kwargs)

    def call(self, *args, **kwargs):
        rep = ""
        for param in self._params:
            if param.name not in kwargs.keys():
                raise exc.MissingCommandInput(self.name, param.name)
            rep += param.tohex(kwargs.pop(param.name))
        return rep

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise exc.ReadOnly('name')

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        raise exc.ReadOnly('number')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        raise exc.ReadOnly('desc')

    @property
    def nparam(self):
        return len(self._params)

    @nparam.setter
    def nparam(self, value):
        raise exc.ReadOnly('nparam')

    @property
    def lparam(self):
        return self._lparam

    @lparam.setter
    def lparam(self, value):
        raise exc.ReadOnly('lparam')

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        raise exc.ReadOnly('level')

    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, value):
        raise exc.ReadOnly('subsystem')

    @property
    def apid(self):
        return self._apid

    @apid.setter
    def apid(self, value):
        raise exc.ReadOnly('apid')

    @property
    def man(self, ret=False):
        if ret:
            return str(self)
        else:
            print(self)

    @man.setter
    def man(self, value):
        raise exc.ReadOnly('man')
