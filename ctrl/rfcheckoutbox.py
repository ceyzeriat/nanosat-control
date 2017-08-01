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


import socket
import select
from byt import Byt
from param import param_all
from .utils import ctrlexception


__all__ = ['RFCheckoutbox']


class RFCheckoutbox(object):
    timeout = float(param_all.RFCHECKOUTBOXTIMEOUT)
    length = int(param_all.RFCHECKOUTBOXLENGTH)

    def __init__(self):
        host = socket.gethostbyname(socket.gethostname())
        self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.port.connect((host, int(param_all.RFCHECKOUTBOXPORT)))
        except:
            self.close()
            raise ctrlexception.RFCheckoutBoxIssue()

    def in_waiting(self):
        return self.length

    def read(self, size=None):
        ready = select.select([self.port], [], [], self.timeout)
        if ready[0]:
            return Byt(self.port.recv(self.length))
        else:
            return None

    def write(self, data):
        if data is not None:
            data = Byt(data)
            if len(data) > 0:
                data = data.replace(param_all.TNCPATHOLOGICCMD,
                                    param_all.TNCPATHOLOGICCMDREPLACE)
                if len(data) > param_all.MAXTCLEN:
                    raise ctrlexception.TCTooLong(len(data)-param_all.MAXTCLEN)
                self.port.sendall(data)

    def close(self):
        self.port.shutdown(socket.SHUT_RDWR)
        self.port.close()
