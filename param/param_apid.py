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


PIDREGISTRATION_OBC_L0 = {  'L0ComManager': 0,
                            'L0MemoryManager': 1,
                            'L0Housekeeper': 2,
                            'L0EpsManager': 3,
                            'L0AdcsManager': 4,
                            'L0SdCardManager': 5,
                            'AdcsManager': 9}

PIDREGISTRATION_OBC_L1 = {  'L1ComManager': 0,
                            'L1EventManager': 1,
                            'L1AdcsManager': 2,
                            'ModeManager': 3,
                            'EventManager': 4}

PIDREGISTRATION_PLD = {     'Bootloader': 0,
                            'BoardDirector': 1,
                            'HkManager': 2,
                            'AcquisitionManager': 3,
                            'PacketsManager': 4,
                            'ObcInterfaceManager': 5,
                            'BeaconManager': 6}


# pid string as key, int as value

# REGISTRATION[pid(string)]
PIDREGISTRATION = {}
PLDREGISTRATION = {}
LVLREGISTRATION = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    PIDREGISTRATION[k.lower()] = v
    PLDREGISTRATION[k.lower()] = '0'
    LVLREGISTRATION[k.lower()] = '0'

for k, v in PIDREGISTRATION_OBC_L1.items():
    PIDREGISTRATION[k.lower()] = v
    PLDREGISTRATION[k.lower()] = '0'
    LVLREGISTRATION[k.lower()] = '1'

for k, v in PIDREGISTRATION_PLD.items():
    PIDREGISTRATION[k.lower()] = v
    PLDREGISTRATION[k.lower()] = '1'
    LVLREGISTRATION[k.lower()] = '1'


# PIDREGISTRATION_REV[pid(int)][payload(int)][level(int)]

# pld, lvl and pid ints as keys, pid string as output
PIDREGISTRATION_REV = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][0] = k.lower()

for k, v in PIDREGISTRATION_OBC_L1.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][1] = k.lower()

for k, v in PIDREGISTRATION_PLD.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][1][1] = k.lower()
