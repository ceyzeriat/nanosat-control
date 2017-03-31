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

from . import cmdexception
from .cm import Cm


__all__ = ['CmADCS']


class CmADCS(Cm):
    def __init__(self, number, name, pid, desc, lparam, subsystem, param,
                    subSystemKey, adcsCommandId):
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
          * subSystemKey (Byt[1]): the hex code of the sub-system
          * adcsCommandId (Byt[1]): the hex code command id from the ADCS
        """
        self.subSystemKey = Byt().fromHex(subSystemKey[:2])
        self.adcsCommandId = Byt().fromHex(adcsCommandId[:2])
        super(CmADCS, self).__init__(number=number, name=name, pid=pid,
                                        desc=desc, lparam=lparam,
                                        subsystem=subsystem, param=param)

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
            inputs[param.name] = kwargs.pop(param.name)
            rep += param.tohex(inputs[param.name])
        if len(rep) != self.lparam and self.lparam is not None:
            raise cmdexception.WrongCommandLength(self.name, len(rep),
                                                    self.lparam)
        rep = Byt('[\x14') + self.subSystemKey + self.adcsCommandId\
                + rep + Byt('][\x15]')
        return rep, inputs

    def to_dict(self):
        """
        Returns a dictionnary for initialization or json dumping
        """
        return {'number': self.number, 'name': self.name, 'pid': self._pidstr,
                'desc': self.desc, 'subsystem': self.subsystem,
                'lparam': self.lparam if self.lparam is not None else "*",
                'param': self._param, 'subSystemKey': str(self.subSystemKey),
                'adcsCommandId': str(self.adcsCommandId)}
"""
    @property
    def adcsCommandId(self):
        return self._adcsCommandId

    @adcsCommandId.setter
    def adcsCommandId(self, value):
        raise cmdexception.ReadOnly('adcsCommandId')

    @property
    def subSystemKey(self):
        return self._subSystemKey

    @subSystemKey.setter
    def subSystemKey(self, value):
        raise cmdexception.ReadOnly('subSystemKey')
"""