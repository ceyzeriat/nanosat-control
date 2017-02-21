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


import time
from threading import Thread
from ctrl.utils import core
from ctrl.utils import Byt
from segsol import listening
from param import param_all


core.prepare_terminal('Listen')
print("Initialization...")
listening.init_listening(antenna=param_all.ANTENNALISTENED)
print("Done\n")

print("Starting...")

if not param_all.FRAMESFLOW:
    while 1:
        time.sleep(0.01)  # Don't kill the CPU
        n = listening.ANTENNA.in_waiting()
        if n < 0:
            continue
        print("n bits read: ", n)
        # grab data
        data = listening.ANTENNA.read(size=n)
        # empty data
        if data is None:
            continue
        if len(data) == 0:
            continue
        listening.report('GotBlob', ll=len(data))
        # deal with it in a separate thread
        loopy = Thread(target=listening.process_data, args=(data,))
        loopy.daemon = True
        loopy.start()
else:
    inbuff = Byt()
    while 1:
        time.sleep(0.01)  # Don't kill the CPU
        n = listening.ANTENNA.in_waiting()
        if n < 0:
            continue
        print("n bits read: ", n)
        # grab data
        data = listening.ANTENNA.read(size=n)
        if data is None:
            continue
        if len(data) == 0:
            continue
        inbuff += data
        res = core.split_flow(inbuff, 1)  # just take first packet
        if len(res) < 2:
            continue  # didn't find a full packet yet
        packet, inbuff = res
        listening.report('GotBlob', ll=len(packet))
        # deal with it in a separate thread
        loopy = Thread(target=listening.process_data, args=(packet,))
        loopy.daemon = True
        loopy.start()
