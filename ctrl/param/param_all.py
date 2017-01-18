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


NOERRORATIMPORT = True

# the path to the file containing the packet id counter
PACKETIDFILE = ["param", "tc_packet_id"]

# the path to the parameter file containing the DB connection settings
DBFILE = ["param", "db_server"]

# who is the emitter
EMITTERID = 1

# who is the receiver
RECEIVERID = 1

# day-reference from unix time
DATETIME_REF = 0  #16801  # 2016,1,1,0,0,0

# little or big endian
TWINKLETWINKLELITTLEINDIA = False

# Global default settings to recieve acknowledgements
REQACKRECEPTION = True
REQACKFORMAT = True
REQACKEXECUTION = True

# the port for telemetry broadcasting/listening
TELEMETRYPORT = 50007
TELEMETRYPORTLISTENERS = 2
SAVELISTENTMNAME = 'save'

# the port for telecommand broadcasting/listening
TELECOMMANDPORT = 50006
TELECOMMANDPORTLISTENERS = 2
COMMLISTENTCNAME = 'comm'

# the port for saving status broadcasting/listening
SAVESTATUSPORT = 50005
SAVESTATUSPORTLISTENERS = 1
WATCHLISTENSAVESTATUSNAME = 'watch'

# the antenna port to listen
ANTENNAPORT = '/dev/ttyS3'

# how often you should listen to the antenna port
ANTENNARPORTREADFREQ = 30

# where the raw telemetry are dumped (locally)
TELEMETRYDUMPFOLDER = ["tm_data"]
# the format of the name for the raw telemetry dumps
TELEMETRYNAMEFORMAT = 'TM_%Y%m%dT%H%M%S_%f.packet'

# the split between filename and data
SOCKETSEPARATOR = "_#;#_"

# the relative path where the raw packets are stored, on the server
RAWPACKETFILDER = './raw_data'
