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


# taken from https://nubes-lesia.obspm.fr/index.php/apps/files?dir=%2FPicSat%2FProjet%2FtrxDoc

# the PID that sends the packets eventually, useful to know for the
# acknowledgement of receipt
PACKETWRAPPERPID = 'L0ComManager'


PIDREGISTRATION_OBC_L0 = {  'L0ComManager': 0,
                            'L0MemoryManager': 1,
                            'L0HouseKeeper': 2,
                            'L0EventProcessor': 3,
                            'L0EpsManager': 4,
                            'L0AdcsManager': 5}

PIDREGISTRATION_OBC_L1 = {  'L1ComManager': 0,
                            'L1EventManager': 1,
                            'L1AdcsManager': 2,
                            'L1ModeManager': 3,
                            'L1EventManager': 4,
                            'payloadManager1': 6,
                            'payloadManager2': 7,
                            'payloadManager3': 8}

PIDREGISTRATION_PLD = {     'hkPayload': 2,
                            'sciencePayload': 3,
                            'debugPayload': 4}


PIDREGISTRATION = {}
PLDREGISTRATION = {}
LVLREGISTRATION = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '0'
    LVLREGISTRATION[k] = '0'

for k, v in PIDREGISTRATION_OBC_L1.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '0'
    LVLREGISTRATION[k] = '1'

for k, v in PIDREGISTRATION_PLD.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '1'
    LVLREGISTRATION[k] = '0'


# PIDREGISTRATION_REV[v][pld][lvl]

PIDREGISTRATION_REV = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][0] = k

for k, v in PIDREGISTRATION_OBC_L1.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][1] = k

for k, v in PIDREGISTRATION_PLD.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][1][1] = k
