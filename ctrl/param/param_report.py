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


REPORTSDATA = [
    ('newRecConnection', "Receiver '{who}' connected to port '{port}'",
        ['who', 'port']),
    ('newTransConnection', "Port '{who}' got a new receiver: '{rec}'",
        ['who', 'rec']),
    ('broadcastTC', "'{who}' broadcasting TC id '{dbid}'",
        ['who', 'dbid']),
    ('sendingTC', "'{who}' is sending TC",
        ['who']),
    ('sentTC', "'{who}' sent TC at '{t}'",
        ['who', 't']),
    ('receivedTM', "'{who}' received data for saving",
        ['who']),
    ('receivedCallsignTM', "'{who}' (callsign '{source}') received data of "\
        "length '{ll}' from callsign '{destination}' for saving",
        ['who', 'source', 'll', 'destination']),
    ('savedTM', "'{who}' saved data under id '{dbid}'",
        ['who', 'dbid']),
    ]
