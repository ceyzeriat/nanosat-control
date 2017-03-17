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
import sys
from byt import Byt
from ctrl.utils import core
from ctrl.utils.report import REPORTS
from ctrl.utils import PIDWatchDog
from ctrl.ccsds import TMUnPacker
from ctrl.ccsds import param_ccsds
from ctrl.xdisp import watchdog
import param
from param import param_category
from param import param_all


__all__ = ['init', 'close']


WATCH_TRANS = None
WATCH_REC_LISTEN = None
WATCH_REC_CONTROL = None
WATCH_REC_SAVE = None
running = False
PIDS = {}


class WatchTrans(hein.SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection is extablished
        """
        broadcast('newTransConnection', who=param_all.WATCHINGNAME,
                    rec=name)


class WatchRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        broadcast('newRecConnection', who=param_all.WATCHINGNAME,
                    port=self.portname)

    def process(self, key, data):
        """
        Sends the data to the antenna
        """
        if key == 'rpt':
            process_report(data)
        elif key == 'dic':
            # comming from control
            if self.portname == param_all.CONTROLLINGNAME:
                # is a full TC broadcast
                if str(data.get(param_all.REPORTKEY,'')) == 'broadcastFullTC':
                    watchdog.XDISP.add_TC(dbid=data.pop('dbid'),
                                    cmdname=data.pop('cmdname'), inputs=data)
        elif key == 'raw':
            pass


def process_report(inputs):
    global PIDS
    key = str(inputs.get(param_all.REPORTKEY))
    broadcast(key, **inputs)
    if key == 'myPID':
        who = inputs['who']
        if who in PIDS.keys():
            killit = PIDS.pop(who)
            killit.stop()
        PIDS[who] = PIDWatchDog(name=who, pid=inputs['pid'],
                                timeout=param_all.PROCESSTIMEOUT,
                                whenDead=revive_process, whenAlive=say_hi,
                                who=who)
    elif key =='broadcastTC':
        pass
    elif key =='GotBlob':
        try:
            hd, hdx, dd = TMUnPacker.unpack(Byt(inputs['blob']),\
                                            retdbvalues=True)
        except:
            print('Tried to unpack.. but an error occurred: {}'\
                    .format(sys.exc_info()[0]))
            return
        pldflag = int(hd[param_ccsds.PAYLOADFLAG.name])
        catnum = int(hd[param_ccsds.PACKETCATEGORY.name])
        # print Header Prim
        print(param_ccsds.HEADER_P_KEYS.disp(hd))
        # print Header Sec TM
        print(param_ccsds.HEADER_S_KEYS_TELEMETRY.disp(hd))
        # print Header Aux if any
        auxtrousseau = param_category.PACKETCATEGORIES[pldflag][catnum]
        if auxtrousseau.size > 0:
            print(auxtrousseau.disp(hdx))
        # print data if any
        datafile = param_category.FILEDATACRUNCHING[pldflag][catnum]
        if datafile is not None:
            print(getattr(param, datafile).TROUSSEAU.disp(dd['unpacked']))
    else:
        pass


def revive_process(who):
    broadcast('IamDead', who=who)
    #PIDS[who].reset()


def say_hi(who):
    broadcast('IamAlive', who=who)


def broadcast(*args, **kwargs):
    """
    Broacasts info
    """
    WATCH_TRANS.tell_report(**kwargs)
    key = str(kwargs.pop(param_all.REPORTKEY, args[0]))
    rpt_verb = REPORTS[key].disp(**kwargs)
    if key not in ['IamDead', 'IamAlive']:
        core.append_logfile(rpt_verb)
        print(rpt_verb)


def init():
    """
    Initializes the control
    """
    global WATCH_TRANS
    global WATCH_REC_LISTEN
    global WATCH_REC_CONTROL
    global WATCH_REC_SAVE
    global running
    if running:
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
    running = True


def close():
    """
    Closes the control
    """
    global WATCH_TRANS
    global WATCH_REC_LISTEN
    global WATCH_REC_CONTROL
    global WATCH_REC_SAVE
    global running
    if not running:
        return
    running = False
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
