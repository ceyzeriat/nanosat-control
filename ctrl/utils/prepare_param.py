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
from param.params import *
from . import ctrlexception


CRC32TABLE = []
for _byte in range(256):
    for _i in range(8):
        _byte = (_byte >> 1) ^ (0xEDB88320 & (-(_byte & 1)))
    CRC32TABLE.append(_byte)

if not JUSTALIB:
    LOGFILE = home_dir(*LOGFILE)
    if not os.path.isfile(LOGFILE):
        open(LOGFILE, mode='w').close()

    TELEMETRYDUMPFOLDER = home_dir(*TELEMETRYDUMPFOLDER)
    if not os.path.exists(TELEMETRYDUMPFOLDER):
        TELEMETRYDUMPFOLDER = None
        if NOERRORATIMPORT:
            print(ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER))
        else:
            raise ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER)


    # if need to transfer the TM on the server
    TELEMETRYSAVEPASS = ''
    if SAVERAWFILE:
        # get pass for telemetry saving to server
        _f = home_dir(*TELEMETRYSAVEPASSFILE)
        try:
            f = open(_f, mode='r')
            TELEMETRYSAVEPASS = f.readline().strip()
            f.close()
            if len(TELEMETRYSAVEPASS) == 0:
                raise IOError
        except IOError:
            if NOERRORATIMPORT:
                print(ctrlexception.MissingServerUserPass(_f))
            else:
                raise ctrlexception.MissingServerUserPass(_f)


    # preparing the DB server
    try:
        f = open(home_dir(*DBFILE), mode='r')
        DBENGINE = f.readline().strip()
        f.close()
        assert len(DBENGINE) > 20
        assert DBENGINE[:13] == 'postgresql://'
    except IOError:
        DBENGINE = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingDBServerFile(home_dir(*DBFILE)))
        else:
            raise ctrlexception.MissingDBServerFile(home_dir(*DBFILE))

    # get password if need be
    for tagname, tag  in PASSTAGS.items():
        if str(DBENGINE).find(tagname) != -1 and tagname != ''\
            and isinstance(tag, list):
            _f = home_dir(*tag)
            try:
                f = open(_f, mode='r')
                DBENGINE = DBENGINE.replace(tagname, f.readline().strip())
                f.close()
            except IOError:
                if NOERRORATIMPORT:
                    print(ctrlexception.MissingDBTagFile(_f, tagname))
                else:
                    raise ctrlexception.MissingDBTagFile(_f, tagname)

    # preparing the source callsign
    _f = home_dir(*CSSOURCEFILE)
    try:
        f = open(_f, mode='r')
        CSSOURCE = f.readline().strip()
        f.close()
    except IOError:
        CSSOURCE = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingSourceCallsign(_f))
        else:
            raise ctrlexception.MissingSourceCallsign(_f)

    # preparing the destination callsign
    _f = home_dir(*CSDESTFILE)
    try:
        f = open(_f, mode='r')
        CSDESTINATION = f.readline().strip()
        f.close()
    except IOError:
        CSDESTINATION = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingDestinationCallsign(_f))
        else:
            raise ctrlexception.MissingDestinationCallsign(_f)

    # packet id file
    PACKETIDFULLFILE = home_dir(*PACKETIDFILE)
    if not os.path.isfile(PACKETIDFULLFILE):
        PACKETIDFULLFILE = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingPacketIDFile(PACKETIDFULLFILE))
        else:
            raise ctrlexception.MissingPacketIDFile(PACKETIDFULLFILE)

    # get the key
    if USESIGGY:
        _f = home_dir(*KEYFILE)
        try:
            f = open(_f, mode='r')
            VITELACLE = Byt().fromHex(f.readline().strip())
            f.close()
        except:
            VITELACLE = None
        if VITELACLE is None or len(VITELACLE) != KEYLENGTH:
            if NOERRORATIMPORT:
                print(ctrlexception.NoControlKey())
            else:
                raise ctrlexception.NoControlKey()

        if sum([int(i) for i in KEYMASK]) != KEYLENGTHCCSDS:
            KEYMASK = '1'*KEYLENGTHCCSDS+'0'*KEYLENGTHCCSDS
            if NOERRORATIMPORT:
                print(ctrlexception.InvalidMask())
            else:
                raise ctrlexception.InvalidMask()


# lookup table for cimputing payload crc
payload_crc_table = {}
poly = 0x04C11DB7

for i in range(256):
    c = i << 24
    for j in range(8):
        c = (c << 1) ^ poly if (c & 0x80000000) else c << 1
    payload_crc_table[i] = c & 0xffffffff
