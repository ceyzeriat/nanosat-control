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


from byt import Byt
from ctrl.soc import SocTransmitter
from ctrl.soc import SocReceiver
from ctrl.utils import core
from ctrl.utils.report import REPORTS
from ctrl.utils import PIDWatchDog
from ctrl.ccsds import TMUnPacker
from ctrl.ccsds import param_ccsds
import param
from param import param_category
from param import param_all


__all__ = ['init_watch', 'close_watch']


WATCH_TRANS = None
WATCH_REC_LISTEN = None
WATCH_REC_CONTROL = None
WATCH_REC_SAVE = None
watch_running = False
PIDS = {}


class WatchTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection is extablished
        """
        broadcast(key='newTransConnection', who=param_all.WATCHINGNAME,
                    rec=name)


class WatchRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        broadcast(key='newRecConnection', who=param_all.WATCHINGNAME,
                    port=self.portname)

    def process(self, data):
        """
        Sends the data to the antenna
        """
        if core.is_reporting(data):
            process_report(data)
        else:
            #hop = core.split_socket_info(data)
            #print("Raw data from '{}'".format(hop['who']))
            pass


def process_report(data):
    global PIDS
    inputs = core.split_socket_info(data, asStr=True)
    key = inputs.pop('key')
    broadcast(key=key, **inputs)
    if key == 'myPID':
        who = inputs['who']
        if who in PIDS.keys():
            killit = PIDS.pop(who)
            killit.stop()
        PIDS[who] = PIDWatchDog(name=who, pid=inputs['pid'],
                                timeout=param_all.PROCESSTIMEOUT,
                                whenDead=revive_process, whenAlive=say_hi,
                                who=who)
    elif key =='GotBlob':
        hd, hdx, dd = TMUnPacker.unpack(Byt(inputs['blob']), retdbvalues=False)
        param_ccsds.disp(hd)
        cat_params = param_category.TABLEDATACRUNCHING.get(\
                            hd[param_ccsds.PACKETCATEGORY.name], None)
        if cat_params is not None:
            getattr(param, cat_params).disp(hdx=hdx, data=dd['all'])
    else:
        pass


def revive_process(who):
    broadcast(key='IamDead', who=who)
    #PIDS[who].reset()


def say_hi(who):
    broadcast(key='IamAlive', who=who)


def broadcast(key, **kwargs):
    """
    Broacasts info
    """
    r = REPORTS[key].disp(**kwargs)
    print('Reporting: {}'.format(r))
    rp = REPORTS[key].pack(**kwargs)
    return WATCH_TRANS.tell(rp)


def init_watch():
    """
    Initializes the control
    """
    global WATCH_TRANS
    global WATCH_REC_LISTEN
    global WATCH_REC_CONTROL
    global WATCH_REC_SAVE
    global watch_running
    if watch_running:
        return
    WATCH_TRANS = WatchTrans(port=param_all.WATCHINGPORT[0],
                             nreceivermax=len(param_all.WATCHINGPORTLISTENERS),
                             start=True, portname=param_all.WATCHINGPORT[1])
    WATCH_REC_LISTEN = WatchRec(port=param_all.LISTENINGPORT[0],
                                    name=param_all.WATCHINGNAME,
                                    connect=True,
                                    connectWait=0.5,
                                    portname=param_all.LISTENINGPORT[1])
    WATCH_REC_CONTROL = WatchRec(port=param_all.CONTROLLINGPORT[0],
                                    name=param_all.WATCHINGNAME,
                                    connect=True,
                                    connectWait=0.5,
                                    portname=param_all.CONTROLLINGPORT[1])
    WATCH_REC_SAVE = WatchRec(port=param_all.SAVINGPORT[0],
                                    name=param_all.WATCHINGNAME,
                                    connect=True,
                                    connectWait=0.5,
                                    portname=param_all.SAVINGPORT[1])
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
    if not watch_running:
        return
    watch_running = False
    WATCH_TRANS.close()
    WATCH_REC_LISTEN.stop_connectLoop()
    WATCH_REC_LISTEN.close()
    WATCH_REC_CONTROL.stop_connectLoop()
    WATCH_REC_CONTROL.close()
    WATCH_REC_SAVE.stop_connectLoop()
    WATCH_REC_SAVE.close()
    WATCH_TRANS = None
    WATCH_REC_LISTEN = None
    WATCH_REC_CONTROL = None
    WATCH_REC_SAVE = None
