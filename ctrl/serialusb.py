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


import serial
import select
from param import param_all
from .utils import Byt
from .utils import ctrlexception


__all__ = ['SerialUSB']


class SerialUSB(object):
    self.timeout = float(param_all.SERIALUSBTIMEOUT)
    self.length = int(param_all.SERIALUSBLENGTH)

    def __init__(self):
        self.port.Serial(param_all.SERIALUSBPORT,
                        baudrate=param_all.SERIALUSBBAUDRATE,
                        parity=param_all.SERIALUSBPARITY)
        self.port.open()
        assert self.port.is_open()
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        self.port.timetout = 0

    def read(self, size=self.length):
        ready = select.select([self.port], [], [], self.timeout)
        if ready[0]:
            return Byt(self.port.read(self.length))
        else:
            return None

    def in_waiting(self):
        return self.port.in_waiting()

    def write(self, data):
        if data is not None:
            data = Byt(data)
            if len(data) > 0:
                self.port.write(data)

    def close(self):
        self.port.close()
