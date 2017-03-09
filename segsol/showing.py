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


import hein
import param
from param import param_all
from ctrl.xdisp.watchdog import XDISP
from ctrl.utils.report import REPORTS


__all__ = ['init', 'close']


SHOW_REC_WATCH = None
running = False
PIDS = {}


class ShowRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        pass

    def process(self, key, data):
        """
        Sends the data to the antenna
        """
        if key == 'rpt':
            key = str(data.pop(param_all.REPORTKEY))
            XDISP.report(REPORTS[key].disp(**data))
        elif key == 'dic':
            #print("Raw data from '{}'".format(data['who']))
            pass


def init():
    """
    Initializes the control
    """
    global SHOW_REC_WATCH
    global XDISP
    global running
    if running:
        return
    SHOW_REC_WATCH = ShowRec(port=param_all.WATCHINGPORT[0],
                                name=param_all.SHOWINGNAME,
                                connect=True,
                                connectWait=0.5,
                                portname=param_all.WATCHINGPORT[1])
    running = True
    XDISP.start()


def close():
    """
    Closes the control
    """
    global SHOW_REC_WATCH
    global XDISP
    global running
    if not running:
        return
    running = False
    SHOW_REC_WATCH.stop_connectLoop()
    SHOW_REC_WATCH.close()
    SHOW_REC_WATCH = None
    ### XDISP = None
