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


from ctrl.utils import Byt


ART = """
  ____  _      ____        _   
 |  _ \(_) ___/ ___|  __ _| |_ 
 | |_) | |/ __\___ \ / _` | __|
 |  __/| | (__ ___) | (_| | |_ 
 |_|   |_|\___|____/ \__,_|\__|
                               
"""

# beep char
BEEP = Byt('\x07')

# to avoid error at import if the DB or folders are not proper
NOERRORATIMPORT = True

# if you don't wanna execute anything at import and just use as a library
JUSTALIB = False

# which antenna are you using
ANTENNALISTENED = 'checkoutbox'

# the path to the file containing the packet id counter
PACKETIDFILE = ['.segsol', 'tc_packet_id']

# the path to the parameter file containing the DB connection settings
DBFILE = ['.segsol', 'db_server']
PASSTAGS = {'<pass>': ['.segsol', 'artichaut']}

# the callsign files
CSSOURCEFILE = ['.segsol', 'callsign_source']
CSDESTFILE = ['.segsol', 'callsign_destination']

# who is the emitter, cf database
EMITTERID = 1  # ['.segsol', 'radio_id']

# who is the receiver, cf database
RECEIVERID = 1  # ['.segsol', 'callsign_source']

# day-reference from unix time
DATETIME_REF = 0  #16801  # 2016,1,1,0,0,0

# little or big endian
TWINKLETWINKLELITTLEINDIA = False

# Global default settings to recieve acknowledgements
REQACKRECEPTION = True
REQACKFORMAT = True
REQACKEXECUTION = True


# process names
LISTENINGNAME = 'listen'  # telemetryport
CONTROLLINGNAME = 'control'
SAVINGNAME = 'save'
WATCHINGNAME = 'watch'


# the port for telemetry broadcasting/listening (alpha)
LISTENINGPORT = (50007, LISTENINGNAME)
LISTENINGPORTLISTENERS = [SAVINGNAME, WATCHINGNAME]

# the port for telecommand broadcasting/listening (beta)
CONTROLLINGPORT = (50006, CONTROLLINGNAME)
CONTROLLINGPORTLISTENERS = [LISTENINGNAME, WATCHINGNAME]

# the port for saving status broadcasting/listening (gamma)
SAVINGPORT = (50005, SAVINGNAME)
SAVINGPORTLISTENERS = [WATCHINGNAME]

# the port for saving status broadcasting/listening (delta)
WATCHINGPORT = (50004, WATCHINGNAME)
WATCHINGPORTLISTENERS = [CONTROLLINGNAME]


# process timeout for the watchdog to get angry
PROCESSTIMEOUT = 5  # sec

# RFCHECKOUTBOX
# port
RFCHECKOUTBOXPORT = 3211
RFCHECKOUTBOXTIMEOUT = 1  # sec
RFCHECKOUTBOXLENGTH = 1024  # octet


# SERIAL
# port 
SERIALUSBPORT = '/dev/ttyS3'
SERIALUSBTIMEOUT = 1  # sec
SERIALUSBLENGTH = 1024  # octet

# where the raw telemetry are dumped (locally), relative to HOME
TELEMETRYDUMPFOLDER = ['tm_data']
# the format of the name for the raw telemetry dumps
TELEMETRYNAMEFORMAT = 'TM_%Y%m%dT%H%M%S_%f.packet'

# the split between keys and data when shipping through sockets
SOCKETSEPARATOR = Byt('###')
SOCKETESCAPE = Byt('/')
SOCKETMAPPER = Byt(':::')
RESPLITVARS = Byt('(?<!') + SOCKETESCAPE + Byt(')') + SOCKETSEPARATOR
RESPLITMAP = Byt('(?<!') + SOCKETESCAPE + Byt(')') + SOCKETMAPPER
REPORTKEY = 'report'


# the relative path where the raw packets are stored, on the server
RAWPACKETFOLDER = './raw_data'
