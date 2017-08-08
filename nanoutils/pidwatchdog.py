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


import os


from .watchdog import WatchDog


__all__ = ['PIDWatchDog']


class PIDWatchDog(WatchDog):
    def __init__(self, name, pid, timeout, whenDead=None, whenAlive=None,
                    **kwargs):
        """
        Creates a watchdog that checks a pid every timeout

        Args:
        * name (str): the name of the watchdog
        * pid (int): the process id to check
        * timeout (int): the time after which the callback function is called
        * whenDead (callable): the handler if the process is found dead
        * whenAlive (callable): the handler if the process is found alive
        """
        self.pid = int(pid)
        self.handlerDead = whenDead\
                            if whenDead is not None and callable(whenDead)\
                            else self.defaultHandler
        self.handlerAlive = whenAlive\
                            if whenAlive is not None and callable(whenAlive)\
                            else None
        super(PIDWatchDog, self).__init__(name=name, timeout=timeout,
                                            handler=self.pidcheck, **kwargs)

    def pidcheck(self, **kwargs):
        """
        Does the pid-checking of the pid
        """
        if is_pid_running(self.pid):
            if callable(getattr(self, "handlerAlive", "")):
                self.handlerAlive(**kwargs)
            self.reset()
        else:
            self.handlerDead(**kwargs)


def is_pid_running(pid):
    try:
        os.kill(pid, 0)
    except:
        return False
    else:
        return True
