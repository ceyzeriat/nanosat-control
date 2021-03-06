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
from nanoparam import param_all_processed as param_all
from nanoutils import param_sys
from nanoctrl.kiss import Framer
from nanoctrl.ccsds import TCUnPacker
from nanoparam import param_ccsds
from nanoctrl.xdisp import watcher
from nanoutils.report import REPORTS


__all__ = ['init', 'close']


SHOW_REC_WATCH = None
running = False
PIDS = {}
XDISP = watcher.XDISP


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
            rpt_key = str(data.pop(param_sys.REPORTKEY, ''))
            if rpt_key == '':
                return
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
            else:
                XDISP.report(REPORTS[rpt_key].disp(**data))
                if rpt_key == 'sentTC':
                    data = data['data']
                    # strip AX25 if need be
                    if param_all.AX25ENCAPS:
                        source, destination, data = Framer.decode_radio(data)
                        # case of the RFCheckoutBox returning garbage
                    if len(data) == 0:
                        return
                    res = TCUnPacker.unpack_primHeader(data)
                    XDISP.set_TC_sent(res[param_ccsds.PACKETID.name], XDISP.OK)
        elif key == 'tcf':
            XDISP.add_TC(packet_id=data[param_ccsds.PACKETID.name], infos=data)
        elif key == 'tmf':
            XDISP.add_TM(packet_id=data[param_ccsds.PACKETID.name], infos=data)


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
                                portname=param_all.WATCHINGPORT[1],
                                hostname = 'localhost')
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
