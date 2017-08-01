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
import socket
import select
import time
from byt import Byt
from param import param_all
from .utils import ctrlexception


__all__ = ['TNCRFBox']


class TNCRFBox(object):
    timeout = float(param_all.TNCRFBOXTIMEOUT)
    length = int(param_all.TNCRFBOXLENGTH)
    ESCAPECHAR = Byt(3)
    NEWLINECHAR = Byt('\r')

    def __init__(self):
        # init write port
        try:
            self.writeport = serial.Serial(param_all.TNCRFBOXWRITEPORT,
                                           baudrate=param_all.TNCRFBOXBAUDRATE)
            assert self.writeport.is_open
        except:
            self.close()
            raise ctrlexception.TNCIssue()
        self.writeport.reset_input_buffer()
        self.writeport.reset_output_buffer()
        self.writeport.timetout = 0
        self.goto_kiss()
        # init read port
        readhost = param_all.TNCRFBOXREADHOST
        self.readport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.readport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.readport.connect((readhost, int(param_all.RFCHECKOUTBOXPORT)))
        except:
            self.close()
            raise ctrlexception.RFCheckoutBoxIssue()

    def goto_kiss(self):
        self.exit_TNCconversation()
        self.exit_TNCconfig()
        # flush random dirt
        self.writeport.write(self.NEWLINECHAR)
        time.sleep(0.1)
        self.writeport.write(Byt('KISS ON') + self.NEWLINECHAR)
        time.sleep(0.1)
        self.writeport.write(Byt('RESTART') + self.NEWLINECHAR)
        time.sleep(1)

    def exit_TNCconversation(self):
        """
        Exits the conversation mode of the TNC
        """
        self.writeport.write(self.ESCAPECHAR)

    def enter_TNCconfig(self):
        """
        Sends the magic word to start config mode
        """
        self.writeport.write(Byt('TC 1;'))

    def exit_TNCconfig(self):
        """
        Sends the magic word to exit config mode
        """
        self.writeport.write(Byt('TC 0;'))

    def set_TNCfrequency(self, config_swap=False):
        """
        Sets the TNC Uplink frequency from the latest G-predict value

        Args:
          * config_swap (bool): if ``False`` sends the frequency command
            straight, else enters/leaves config mode before/after sending
        """
        if config_swap:
            self.enter_TNCconfig()
        self.writeport.write(Byt('FB;'))
        if config_swap:
            self.exit_TNCconfig()

    def read(self, size=None):
        ready = select.select([self.readport], [], [], self.timeout)
        if ready[0]:
            return Byt(self.readport.recv(self.length))
        else:
            return None

    def in_waiting(self):
        return self.length

    def write(self, data):
        if data is not None:
            data = Byt(data)
            if len(data) > 0:
                self.set_TNCfrequency(config_swap=True)
                # escaping of pathologic TNC phrase 'TC '
                data = data.replace(param_all.TNCPATHOLOGICCMD,
                                    param_all.TNCPATHOLOGICCMDREPLACE)
                if len(data) > param_all.MAXTCLEN:
                    raise ctrlexception.TCTooLong(len(data)-param_all.MAXTCLEN)
                self.writeport.write(data)

    def close(self):
        self.writeport.close()
        self.readport.shutdown(socket.SHUT_RDWR)
        self.readport.close()
