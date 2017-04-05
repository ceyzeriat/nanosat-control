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


__all__ = ['REPORTSDATA']


EXTRADISPKEY = "prt"


# report_key, disp phrase fmt, params [, print flag]

REPORTSDATA = [
    ('newRecConnection', "Receiver '{who}' connected to port '{port}'",
        ['who', 'port']),
    ('newTransConnection', "Port '{who}' got a new receiver: '{rec}'",
        ['who', 'rec']),
    ('broadcastTC', "'{who}' broadcasting TC '{cmdname}' dbid '{dbid}'",
        ['who', 'dbid', 'cmdname']),
    ('sendingTC', "'{who}' is sending TC",
        ['who']),
    ('sentTC', "'{who}' sent TC at '{t}'",
        ['who', 't', 'data']),
    ('receivedTM', "'{who}' received data for saving",
        ['who']),
    ('receivedCallsignTM', "'{who}' (callsign '{source}') received data of "\
        "length '{ll}' from callsign '{destination}' for saving",
        ['who', 'source', 'll', 'destination']),
    ('savedTM', "'{who}' saved data under dbid '{dbid}'",
        ['who', 'dbid']),
    ('myPID', "'{who}' has PID '{pid}'",
        ['who', 'pid']),
    ('IamDead', "Process '{who}' is dead",
        ['who'], False),
    ('IamAlive', "Process '{who}' is alive",
        ['who'], False),
    ('receivedRawTM', "'{who}' received CCSDS-flow data of length '{ll}' "\
        "for saving",
        ['who', 'll']),
    ('GotBlob', "'{who}' got blob of data of len '{ll}'",
        ['who', 'll', 'blob']),
    ('SettingUpAntenna', "Setting up antenna '{antenna}'",
        ['who', 'antenna']),
    ('gotACK', "Got acknowledment",
        ['who', 'pkid', 'thecat', 'error'], False)
    ]
