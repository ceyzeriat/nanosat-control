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
from ctrl.ccsds import TCUnPacker
from ctrl.ccsds import param_ccsds
from ctrl.xdisp import watchdog as wt
from ctrl.utils.report import REPORTS


__all__ = ['init', 'close']


SHOW_REC_WATCH = None
running = False
PIDS = {}
XDISP = wt.XDISP


class ShowRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        pass

    def process(self, key, data):
        """
        Updates the XDISP window
        """
        if key == 'rpt':
            rpt_key = str(data.pop(param_all.REPORTKEY, ''))
            who = str(data['who'])
            if rpt_key == 'IamDead':
                if who == param_all.CONTROLLINGNAME:
                    XDISP.set_controlico(XDISP.DEAD)
                elif who == param_all.LISTENINGNAME:
                    XDISP.set_listenico(XDISP.DEAD)
                elif who == param_all.SAVINGNAME:
                    XDISP.set_saveico(XDISP.DEAD)
            elif rpt_key == 'IamAlive':
                if who == param_all.CONTROLLINGNAME:
                    XDISP.set_controlico(XDISP.ALIVE)
                elif who == param_all.LISTENINGNAME:
                    XDISP.set_listenico(XDISP.ALIVE)
                elif who == param_all.SAVINGNAME:
                    XDISP.set_saveico(XDISP.ALIVE)
            elif rpt_key == 'sentTC':
                res = TCUnPacker.unpack_primHeader(data['data'])
                XDISP.set_TC_sent(res[param_ccsds.PACKETID.name], XDISP.OK)
            elif rpt_key == 'gotACK':
                thecat = str(data['thecat'])
                error = str(data['error'])
                if thecat == '0':  # RACK
                    XDISP.set_TC_rack(str(data['pkid']),
                                      XDISP.OK)
                elif thecat == '1':  # FACK
                    XDISP.set_TC_fack(str(data['pkid']),
                                      XDISP.ERROR if error != '0'\
                                                    else XDISP.OK)
                elif thecat == '2':  # EACK
                    XDISP.set_TC_eack(str(data['pkid']),
                                      XDISP.ERROR if error != '0'\
                                                    else XDISP.OK)
            elif rpt_key == '':
                pass
            else:
                XDISP.report(REPORTS[rpt_key].disp(**data))
        elif key == 'tcf':
            XDISP.add_TC(dbid=data.get('dbid'),
                            cmdname=data.get('cmdname'), infos=data)


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
