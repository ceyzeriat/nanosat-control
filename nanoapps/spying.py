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
import hein
from nanoparam import param_all_processed as param_all


__all__ = ['process_data', 'init', 'close']


# the path where to create the directories in which packets data will be stored
ALL_TEL = 'all_telemetries'
# the name of the dir
DIRNAME = None

SPY_REC = None
SPY_TRANS = None
running = False



class SpyTrans(hein.SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """

class SpyRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """

    def process(self, key, data):
        """
        Saves the packet on the disk 
        """
        # ignores the reporting
        if key == 'rpt':
            return
        process_data(data)
        return

    
def process_data(data):
    """
    A callback function that saves the package and sends it
    over the TM socket
    """
    if len(data) == 0:
        return
    filename = os.path.split(str(data['path']))[1]
    local_path = os.path.join(DIRNAME, 'tm_data', filename)
    print("Spying: '{}' >> {}".format(data['data'].hex(), local_path))
    # locally saved
    f = open(param_all.Pathing('~', ALL_TEL, local_path).path, mode='wb')
    f.write(data['data'])
    f.close()
    SPY_TRANS.tell_dict(**data)

    
def init(dir_name):
    """
    Initializes the spying
    """
    global SPY_REC
    global SPY_TRANS    
    global running
    global DIRNAME
    if running:
        return
    DIRNAME = str(dir_name).lstrip(os.sep)
    sub_dir = param_all.Pathing('~', ALL_TEL, DIRNAME)
    if sub_dir.exists:
        print("Directory '{}' already exists. Please change the name!"\
                                                        .format(sub_dir.path))
    else:
        os.mkdir(sub_dir.path)
        os.mkdir(param_all.Pathing(sub_dir, 'tm_data').path)
        SPY_TRANS = SpyTrans(port=param_all.SPYINGPORT[0],
                             nreceivermax=5,
                             start=True,
                             portname=param_all.SPYINGPORT[1],
                             timeoutACK=3)        
        SPY_REC = SpyRec(port=param_all.LISTENINGPORT[0],
                                name=param_all.SPYINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.LISTENINGPORT[1],
                                hostname = 'localhost')
        running = True


def close():
    """
    Closes the listening
    """
    global SPY_REC
    global SPY_TRANS    
    global running
    if not running:
        return
    running = False
    SPY_TRANS.close()    
    SPY_REC.stop_connectLoop()
    SPY_REC.close()
    SPY_REC = None
