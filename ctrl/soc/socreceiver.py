#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
from threading import Thread
import select
import time


__all__ = ['SocReceiver']


class SocReceiver(object):
    def __init__(self, port, name, buffer_size=1024, connect=True,
                    connectWait=0.5):
        """
        Connects to a transmitting port in order to listen for
        any communication from it. In case the communication drops
        it will try to reconnect periodically.

        Args:
        * port (int): the communication port
        * name (str[15]): the name of the receiver, for identification
          purposes
        * buffer_size (int): the size in octet of each listening
        * connect (bool): whether to start the connection loop
          at initialization. If ``False``, use ``connect`` method.
        * connectWait (float >0.1): the duration in second between two
          successive connection attempts
        """
        self.buffer_size = int(buffer_size)
        self._soc = None
        self._loopConnect = False
        self._connected = False
        self._timeout = 1.
        self.name = str(name)[:15]
        self._running = False
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = int(port)
        self._connectWait = max(0.1, float(connectWait))
        self.connect(oneshot=True)

    def __str__(self):
        return "Socket receiver on port {:d} ({})".format(
            self.port,
            'on' if self.connected and self.running else 'off')

    __repr__ = __str__

    def _receive(self, transmitter, l=15, timeout=None):
        timeout = self._timeout if timeout is None else float(timeout)
        ready = select.select([transmitter], [], [], timeout)
        if ready[0]:
            return transmitter.recv(int(l))
        else:
            return None

    @property
    def connected(self):
        """
        Whether the receiver is connected to the transmitter
        """
        try:
            self._soc.getpeername()
        except:
            return False
        return True

    @connected.setter
    def connected(self, value):
        pass

    @property
    def loopConnect(self):
        return self._loopConnect

    @loopConnect.setter
    def loopConnect(self, value):
        pass

    def connect(self, oneshot=False):
        """
        If not already connected, starts the connection loop
        """
        if self.loopConnect:
            return
        self._loopConnect = True
        loopy = Thread(target=connectme, args=(self, oneshot))
        loopy.daemon = True
        loopy.start()

    def stop_connectLoop(self):
        """
        Stops the connection loop, but does not stop the current
        connection nor communication 
        """
        self._loopConnect = False
        time.sleep(self._connectWait)

    @property
    def running(self):
        """
        Whether the listening is undergoing
        """
        return self._running

    @running.setter
    def running(self, value):
        pass

    def _start(self):
        if not self.running and self.connected:
            self._running = True
            loopy = Thread(target=tellme, args=(self, ))
            loopy.daemon = True
            loopy.start()
            return True
        else:
            return False

    def close(self):
        """
        Shuts down the receivers. Use 
        """
        if not self.running:
            return
        self._running = False
        self._soc.shutdown(socket.SHUT_RDWR)
        self._soc.close()
        self._soc = None

    def process(self, data):
        """
        Replace this function with proper data processing
        """
        print(data)

    def _newconnection(self):
        """
        Replace this function with proper new connection processing
        """
        print(self._soc)

    def _get_AR(self):
        """
        Returns ``True`` if the transmitter got the message else
        ``Flase``
        """
        return self._receive(self._soc, l=1, timeout=self._timeout) == '0'


def tellme(self):
    """
    Infinite loop to listen the data from the port
    """
    while self.running:
        data = self._soc.recv(self.buffer_size)
        if data == '' or not self.running:
            self.close()
            return
        self._soc.sendall('0')
        if data == '__die__':
            self.close()
        else:
            self.process(data)


def connectme(self, oneshot):
    """
    Infinite loop to listen the data from the port
    """
    while self.loopConnect or oneshot:
        oneshot = False
        if self.connected:
            time.sleep(self._connectWait)
            continue
        if self._soc is None:
            self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._soc.connect((self.host, self.port))
            ready = True
        except:
            if not self.loopConnect:
                return False
            ready = False
        if ready:
            if not self._get_AR():
                if not self.loopConnect:
                    return False
            else:
                self._soc.sendall(self.name)
                if not self._get_AR():
                    self.close()
                    if not self.loopConnect:
                        return False
                else:
                    status = self._start()
                    self._newconnection()
                    if not self.loopConnect:
                        return status
        time.sleep(self._connectWait)
