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
from ctrl.utils.report import REPORTS, EXTRADISPKEY
from ctrl.utils import PIDWatchDog
from ctrl.ccsds import TMUnPacker
from ctrl.ccsds import param_ccsds
from ctrl.kiss import Framer
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
        elif key == 'tcf':  # full TC from control
            # just pass it over
            WATCH_TRANS.tell_key('tcf', **data)
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
        # restart watchdog PID with new PID number
        PIDS[who] = PIDWatchDog(name=who, pid=inputs['pid'],
                                timeout=param_all.PROCESSTIMEOUT,
                                whenDead=revive_process, whenAlive=say_hi,
                                who=who)
    elif key =='broadcastTC':
        pass
    elif key =='GotBlob':
        blobish = Byt(inputs['blob'])
        try:
            # strip AX25 if need be
            if param_all.AX25ENCAPS:
                source, destination, blobish = Framer.decode_radio(blobish)
                # case of the RFCheckoutBox returning garbage
                if len(blobish) == 0:
                    print('That was junk from RFCheckoutBox')
                    return
            if len(blobish) == 0:
                print("Can't unpack empty packet")
                return
            hd, hdx, dd = TMUnPacker.unpack(blobish)
        except:
            print('Tried to unpack.. but an error occurred: {}'\
                    .format(sys.exc_info()[0]))
            return
        inpacket = dict(hd)
        inpacket.update(hdx)
        inpacket.update(dd)
        inpacket['sz'] = len(blobish)
        WATCH_TRANS.tell_key('tmf', **inpacket)
        pldflag = int(hd[param_ccsds.PAYLOADFLAG.name])
        catnum = int(hd[param_ccsds.PACKETCATEGORY.name])
        # print Header Prim
        print(param_ccsds.HEADER_P_KEYS.disp(hd))
        # print Header Sec TM
        print(param_ccsds.HEADER_S_KEYS_TELEMETRY.disp(hd))
        # print Header Aux if any
        cat = param_category.CATEGORIES[pldflag][catnum]
        if cat.aux_size > 0:
            print(cat.aux_trousseau.disp(hdx))
        # print data if any
        if cat.data_trousseau is not None:
            print(cat.data_trousseau.disp(dd['unpacked'], hds=hd, hdx=hdx))
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
    kwargs[param_all.REPORTKEY] = str(args[0])
    WATCH_TRANS.tell_report(**kwargs)
    key = kwargs.pop(param_all.REPORTKEY)
    rpt_verb = REPORTS[key].disp(**kwargs)
    core.append_logfile(rpt_verb)
    if kwargs.get(EXTRADISPKEY, REPORTS[key].prt):
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
                                    portname=param_all.LISTENINGPORT[1],
                                    hostname = 'localhost')
    WATCH_REC_CONTROL = WatchRec(port=param_all.CONTROLLINGPORT[0],
                                    name=param_all.WATCHINGNAME,
                                    connect=True,
                                    connectWait=0.5,
                                    portname=param_all.CONTROLLINGPORT[1],
                                    hostname = 'localhost')
    WATCH_REC_SAVE = WatchRec(port=param_all.SAVINGPORT[0],
                                    name=param_all.WATCHINGNAME,
                                    connect=True,
                                    connectWait=0.5,
                                    portname=param_all.SAVINGPORT[1],
                                    hostname = 'localhost')
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
