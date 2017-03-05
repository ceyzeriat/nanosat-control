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
from threading import Thread
import select
import time


__all__ = ['SocTransmitter']


ACK = "\xaa"


class SocTransmitter(object):
    def __init__(self, port, nreceivermax, start=True, portname=""):
        """
        Creates a transmitting socket to which receiving socket
        can listen.

        Args:
        * port (int): the communication port
        * nreceivermax (int): the maximum amount of receivers that can
          listen. From 1 to 5.
        * start (bool): whether to start the broadcasting at
          initialization or not. If not, use ``start`` method
        * portname (str[15]): the name of the communicating port, for
          identification purposes
        """
        self._running = False
        self.port = int(port)
        self.portname = str(portname)[:15]
        self._nreceivermax = max(1, min(5, int(nreceivermax)))
        self.receivers = {}
        self.sending_buffer = []
        if start:
            self.start()

    def __str__(self):
        return "Socket transmitter on port {:d} ({})".format(
            self.port,
            'on' if self.running else 'off')

    __repr__ = __str__
    
    def start(self):
        """
        Initializes and starts the broadcasting on the communication
        port, if not already started.
        """
        if self.running:
            return
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._soc.setblocking(0)
        self._soc.bind(('', self.port))
        self._soc.listen(self._nreceivermax)
        self._running = True
        loopy = Thread(target=accept_receivers, args=(self,))
        loopy.daemon = True
        loopy.start()
        loopy = Thread(target=send_buffer, args=(self,))
        loopy.daemon = True
        loopy.start()

    @property
    def nreceivers(self):
        """
        The number of receivers currently listening to the port.
        Note that the active receivers are updated at each communication
        and some receivers may have dropped since then
        """
        return len(self.receivers)

    @nreceivers.setter
    def nreceivers(self, value):
        return

    def _tell_receiver(self, name, receiver, txt):
        try:
            receiver.getpeername()
        except:
            return
        receiver.sendall(txt)
        if not self._receive(receiver, l=1, timeout=0.1) == ACK:
            del self.receivers[name]

    def _receive(self, receiver, l=15, timeout=None):
        timeout = self._timeout if timeout is None else float(timeout)
        ready = select.select([receiver], [], [], timeout)
        if ready[0]:
            return receiver.recv(int(l))
        else:
            return None

    def tell(self, txt):
        """
        Broadcasts a message to all receivers, and consequently
        updates the list of active receivers.
        Note: ``__die__`` is a reserved message that will kill the
        receivers

        Args:
        * txt (str): the message
        """
        if not self.running:
            return False
        if len(txt) == 0:
            return None
        self.sending_buffer.append(str(txt))
        return True

    def close_receivers(self):
        """
        Forces all receivers to drop listening
        """
        self.tell('__die__')
        self.receivers = {}

    def close(self):
        """
        Shuts the broadcasting down, and forces all receivers to
        drop listening. The broadcasting can be restarted using
        ``start``.
        """
        if not self.running:
            return
        self.sending_buffer = []
        self._running = False
        self.close_receivers()
        self._soc.shutdown(socket.SHUT_RDWR)
        self._soc.close()

    @property
    def running(self):
        """
        Whether the broadcasting is active or not
        """
        return self._running

    @running.setter
    def running(self, value):
        pass

    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished

        Can be overriden, although ``name`` parameter is mandatory
        """
        print('hello: {}'.format(name))


def send_buffer(self):
    """
    Infinite loop sending messages
    """
    while self.running:
        # make a list-copy
        for line in list(self.sending_buffer):
            # make a list-copy
            for name, receiver in list(self.receivers.items()):
                self._tell_receiver(name, receiver, line)
            del self.sending_buffer[0]
            time.sleep(0.03)
        # crash of process
        try:
            time.sleep(0.01)
        except:
            pass


def accept_receivers(self):
    """
    Infinite loop registering all new receivers
    """
    while self.running:
        receiver = None
        # blocking with 1 sec timeout
        ready = select.select([self._soc], [], [], 1)
        if ready[0]:
            # should be a new connection here, but just in case...
            try:
                receiver, addr = self._soc.accept()
            except:
                continue
        else:
            continue
        # maybe _soc broke while select
        if not self.running:
            receiver.shutdown(socket.SHUT_RDWR)
            receiver.close()
            break
        trusty = True
        if self.nreceivers >= self._nreceivermax:
            # maybe replace old droped connection with new one
            trusty = False
        receiver.send(ACK)
        name = self._receive(receiver, l=15, timeout=5.)
        if name is not None:
            if not trusty:  # replace old connection
                if name not in self.receivers:  # name does not exist already
                    receiver.shutdown(socket.SHUT_RDWR)
                    receiver.close()
                else:
                    # close broken socket
                    self.receivers[name].shutdown(socket.SHUT_RDWR)
                    self.receivers[name].close()
                    receiver.send(ACK)
                    self.receivers[name] = receiver
                    self._newconnection(name)
            else:
                if name not in self.receivers:
                    receiver.send(ACK)
                    self.receivers[name] = receiver
                    self._newconnection(name)
                else:  # redundant socket name
                    pass
        else:
            receiver.shutdown(socket.SHUT_RDWR)
            receiver.close()
