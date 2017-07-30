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


from threading import Timer
from . import ctrlexception


__all__ = ['WatchDog']


class WatchDog(object):
    def __init__(self, name, timeout, handler=None, **kwargs):
        """
        Creates a watchdog based on a timer

        Args:
        * name (str): the name of the watchdog
        * timeout (int): the time after which the callback function is called
        * handler (callable): the handler in case of timeout

        Kwargs:
        * passed on to handler
        """
        self.name = str(name)
        self.timeout = timeout
        self.handler = handler\
                        if handler is not None and callable(handler)\
                            else self.defaultHandler
        self._kwargs = kwargs
        self._start(self.handler, **self._kwargs)

    def _start(self, handler=None, **kwargs):
        """
        Starts the watchdog timer

        Kwargs:
        * passed on to handler
        """
        handler = self.handler if handler is None else handler
        self.timer = Timer(self.timeout, handler, kwargs=self._kwargs)
        self.timer.start()

    def reset(self, **kwargs):
        """
        Resets the watchdog timer

        Kwargs:
        * passed on to handler
        """
        self._kwargs.update(kwargs)
        self.stop()
        self._start(self.handler, **self._kwargs)

    def stop(self):
        """
        Stops the watchdog timer
        """
        self.timer.cancel()

    def defaultHandler(self, **kwargs):
        """
        Default callback function raising Watchdog
        """
        raise ctrlexception.WatchDogTimeOut(self.name)
