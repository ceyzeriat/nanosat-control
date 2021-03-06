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
from nanoparam import param_apid
from nanoparam.commands import param_commands
from nanoutils import fcts


from . import cmdexception
from .parameter import Parameter


__all__ = ['Cm']


class Cm(object):
    def __init__(self, number, name, pid, desc, lparam, subsystem, param):
        """
        Creates a self-checking command
        
        Args:
          * number (int): the unique id
          * name (str): the name (code friendly)
          * pid (str): the unique pid identity string
          * desc (str): the description
          * lparam (int): the total length of the parameters, in
            octets, or "*" for any
          * subsystem (str): the subsystem key
          * param (iterable of list): an iterable of parameter lists of
            form and order: (name, desc, rng, typ, size, unit)
        """
        self._name = fcts.clean_name(name)
        self._number = int(number)
        pid = str(pid).lower()
        if pid not in param_apid.PIDREGISTRATION.keys():
            raise cmdexception.WrongPID(pid, self.name)
        self._pidstr = pid
        self._pid = int(param_apid.PIDREGISTRATION[pid])
        self._payload = int(param_apid.PLDREGISTRATION[pid])
        self._level = int(param_apid.LVLREGISTRATION[pid])
        self._desc = str(desc)
        self._lparam = int(lparam) if lparam != "*" else None
        self._subsystem = str(subsystem)
        self._param = [tuple(item) for item in param]
        self._params = []
        for idx, item in enumerate(self._param):
            if len(item) < param_commands.MINLENPARAMSTRUCTURE:
                raise cmdexception.WrongParameterDefinition(item[0], 'all')
            p = Parameter(*item)
            self._params.append(p)
            setattr(self, "p_{}_{}".format(idx, p.name), self._params[-1])
        self._nparam = len(self._params)

    def __str__(self):
        return "#{} {} (L{}, pid: {})\n {}\n{} params: ({} octet)\n{}".format(
                            self.number,
                            self.name,
                            int(self.level),
                            self._pidstr,
                            self.desc,
                            self.nparam,
                            self.lparam if self.lparam is not None else "*",
                            "\n".join([str(item) for item in self._params]))

    def __repr__(self):
        return self.__str__()

    def __call__(self, *args, **kwargs):
        return _wrapcall(**kwargs)

    def _wrapcall(self, *args, **kwargs):
        return self.generate_data(**kwargs)

    def to_dict(self):
        """
        Returns a dictionnary for initialization or json dumping
        """
        return {'number': self.number, 'name': self.name, 'pid': self._pidstr,
                'desc': self.desc, 'subsystem': self.subsystem,
                'lparam': self.lparam if self.lparam is not None else "*",
                'param': self._param}

    def generate_data(self, *args, **kwargs):
        """
        Returns the packet data (as string) and the dictionnary of
        input parameters => values. The input parameters are that of
        the command, see ``man`` method.

        Args are ignored

        Kwargs: the input parameters of the command
        """
        rep = Byt()
        inputs = {}
        for param in self._params:
            if param.name not in kwargs.keys():
                raise cmdexception.MissingCommandInput(self.name, param.name)
            if param.typ.typ.lower() == 'str':
                inputs[param.name] = Byt(kwargs[param.name])
            else:    
                inputs[param.name] = kwargs[param.name]
            rep += param.tohex(inputs[param.name])
        if len(rep) != self.lparam and self.lparam is not None:
            raise cmdexception.WrongCommandLength(self.name, len(rep),
                                                    self.lparam)
        return rep, inputs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise cmdexception.ReadOnly('name')

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        raise cmdexception.ReadOnly('number')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        raise cmdexception.ReadOnly('desc')

    @property
    def nparam(self):
        return self._nparam

    @nparam.setter
    def nparam(self, value):
        raise cmdexception.ReadOnly('nparam')

    @property
    def lparam(self):
        return self._lparam

    @lparam.setter
    def lparam(self, value):
        raise cmdexception.ReadOnly('lparam')

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        raise cmdexception.ReadOnly('level')

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        raise cmdexception.ReadOnly('payload')

    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, value):
        raise cmdexception.ReadOnly('subsystem')

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        raise cmdexception.ReadOnly('pid')

    @property
    def man(self):
        print(self)

    @man.setter
    def man(self, value):
        raise cmdexception.ReadOnly('man')

    @property
    def ex(self):
        params = []
        for p in self._params:
            params.append("{}= ".format(p.name))
        print("c.{}({})".format(self.name, ', '.join(params)))

    @ex.setter
    def ex(self, value):
        raise cmdexception.ReadOnly('ex')
    
    @property
    def exval(self):
        params = []
        for p in self._params:
            if p.exval is not None:
                v = p.exval
            else:
                v = p.rng[0]
                if p.typ.typ == 'str':
                    # transform into char if string
                    v = chr(v) * p.size
                else:
                    sz = p.size if isinstance(p.size, int) else 5
                    if sz > 1:
                        v = [v] * sz
                v = repr(v)
            params.append("{}={}".format(p.name, v))
        print("c.{}({})".format(self.name, ', '.join(params)))

    @exval.setter
    def exval(self, value):
        raise cmdexception.ReadOnly('exval')
