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
from .utils import core


__all__ = ['RFCheckoutbox']


class RFCheckoutbox(object):
    def __init__(self):
        host = socket.gethostbyname(socket.gethostname())
        port = int(23)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.connect((host, port))

    def in_waiting(self, ):
        pass

    def read(self, ):
        pass

    def write(self, ):
        pass

    def close(self, ):
        pass


"""
import select


port = 3211
timeout = 1
l = 999



data = []
while 1:
    ready = select.select([soc], [], [], timeout)
    if ready[0]:
        data.append(soc.recv(int(l)))
        print(data)
    else:
        print('maybe next time')
"""