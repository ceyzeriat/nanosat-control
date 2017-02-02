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


from ..utils import Byt


#SERIAL_TIMEOUT = 0.01
#READ_BYTES = 1000

# KISS Special Characters
# http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
# http://k4kpk.com/content/notes-aprs-kiss-and-setting-tnc-x-igate-and-digipeater
# Frames begin and end with a FEND/Frame End/0xC0 byte
FEND = Byt('\xc0')  # Marks START and END of a Frame
FESC = Byt('\xdb')  # Escapes FEND and FESC bytes within a frame

# Transpose Bytes: Used within a frame-
# "Transpose FEND": An FEND after an FESC (within a frame)-
# Sent as FESC TFEND
TFEND = Byt('\xdc')
# "Transpose FESC": An FESC after an FESC (within a frame)-
# Sent as FESC TFESC
TFESC = Byt('\xdd')

# "FEND is sent as FESC, TFEND"
# 0xC0 is sent as 0xDB 0xDC
FESC_TFEND = Byt().join([FESC, TFEND])

# "FESC is sent as FESC, TFESC"
# 0xDB is sent as 0xDB 0xDD
FESC_TFESC = Byt().join([FESC, TFESC])

# KISS Command Codes
# http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
DATA_FRAME = Byt('\x00')
SLOT_TIME = Byt('\x03')
#TX_DELAY = Byt('\x01')
#PERSISTENCE = Byt('\x02')
#TX_TAIL = Byt('\x04')
#FULL_DUPLEX = Byt('\x05')
#SET_HARDWARE = Byt('\x06')
#RETURN = Byt('\xFF')


#DEFAULT_KISS_CONFIG_VALUES = {
#    'TX_DELAY': 40,
#    'PERSISTENCE': 63,
#    'SLOT_TIME': 20,
#    'TX_TAIL': 30,
#    'FULL_DUPLEX': 0,
#}

#KISS_ON = Byt('KISS $0B')
#KISS_OFF = Byt().join([FEND, Byt('\xff'), FEND, FEND])

#NMEA_HEADER = Byt().join([FEND, Byt('\xf0'), Byt('$')])



#APRSIS_SERVER = 'rotate.aprs.net'
#APRSIS_FILTER_PORT = 14580
#APRSIS_RX_PORT = 8080

#APRSIS_SW_VERSION = Byt('APRS Python Module')
#APRSIS_URL = 'http://srvr.aprs-is.net:8080'

#APRSIS_HTTP_HEADERS = {
#    'content-type': 'application/octet-stream',
#    'accept': 'text/plain'
#}

#RECV_BUFFER = 1024
