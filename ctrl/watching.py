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


from .soc import SocTransmitter
from .soc import SocReceiver
from .utils import core


__all__ = ['init_watch', 'close_watch']


WATCH_TRANS = None
WATCH_REC_LISTEN = None
WATCH_REC_CONTROL = None
WATCH_REC_SAVE = None
watch_running = False


class WatchTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        r = REPORTS['newTransConnection'].disp(who=core.WATCHINGNAME, rec=name)
        print(r)


class WatchListenRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        r = REPORTS['newRecConnection'].disp(who=core.WATCHINGNAME,
                                                port=self.portname)
        print(r)

    def process(self, data):
        """
        Sends the data to the antenna
        """
        if core.is_reporting(data):
            inputs = core.split_socket_info(data)
            print('Reporting: '+REPORTS[inputs['key']].disp(**inputs))
        else:
            print('Raw data: '+repr(data))


class WatchControlRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        r = REPORTS['newRecConnection'].disp(who=core.WATCHINGNAME,
                                                port=self.portname)
        print(r)

    def process(self, data):
        """
        Sends the data to the antenna
        """
        if core.is_reporting(data):
            inputs = core.split_socket_info(data)
            print('Reporting: '+REPORTS[inputs['key']].disp(**inputs))
        else:
            print('Raw data: '+repr(data))


class WatchSavingRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        r = REPORTS['newRecConnection'].disp(who=core.WATCHINGNAME,
                                                port=self.portname)
        print(r)

    def process(self, data):
        """
        Sends the data to the antenna
        """
        if core.is_reporting(data):
            inputs = core.split_socket_info(data)
            print('Reporting: '+REPORTS[inputs['key']].disp(**inputs))
        else:
            print('Raw data: '+repr(data))


def init_watch():
    """
    Initializes the control
    """
    global WATCH_TRANS
    global WATCH_REC_LISTEN
    global WATCH_REC_CONTROL
    global WATCH_REC_SAVE
    global watch_running
    WATCH_TRANS = WatchTrans(port=core.WATCHINGPORT[0],
                                nreceivermax=len(core.WATCHINGPORTLISTENERS),
                                start=True, portname=core.WATCHINGPORT[1])
    WATCH_REC_LISTEN = WatchTMRec(port=core.LISTENINGPORT,
                                name=core.WATCHINGNAME, connect=True,
                                connectWait=0.5, portname=core.WATCHINGPORT[1])
    WATCH_REC_CONTROL = WatchTCRec(port=core.CONTROLLINGPORT,
                                name=core.WATCHINGNAME, connect=True,
                                connectWait=0.5, portname=core.WATCHINGPORT[1])
    WATCH_REC_SAVE = WatchSTRec(port=core.SAVINGPORT,
                                name=core.WATCHINGNAME, connect=True,
                                connectWait=0.5, portname=core.WATCHINGPORT[1])
    watch_running = True


def close_watch():
    """
    Closes the control
    """
    global WATCH_TRANS
    global WATCH_REC_LISTEN
    global WATCH_REC_CONTROL
    global WATCH_REC_SAVE
    global watch_running
    watch_running = False
    WATCH_TRANS.close()
    WATCH_TRANS = None
    WATCH_REC_LISTEN = None
    WATCH_REC_CONTROL = None
    WATCH_REC_SAVE = None
