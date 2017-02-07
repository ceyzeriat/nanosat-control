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
from ..param.param_all import *
from . import ctrlexception


MAXPACKETID = 2**14

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME = os.path.expanduser("~")

def concat_dir(*args):
    """
    Concatenates the path in ``args`` into a string-path
    """
    return os.path.join(*args)

def rel_dir(*args):
    """
    Concatenates the path in ``args`` into a relative
    string-path from the package directory
    """
    return concat_dir(ROOT, *args)

if not JUSTALIB:
    TELEMETRYDUMPFOLDER = concat_dir(HOME, *TELEMETRYDUMPFOLDER)
    if not os.path.exists(TELEMETRYDUMPFOLDER):
        TELEMETRYDUMPFOLDER = None
        if NOERRORATIMPORT:
            print(ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER))
        else:
            raise ctrlexception.BrokenTelemetryDumpFolder(TELEMETRYDUMPFOLDER)

    # preparing the DB server
    try:
        f = open(rel_dir(*DBFILE), mode='r')
        DBENGINE = f.readline().strip()
        f.close()
        assert len(DBENGINE) > 20
        assert DBENGINE[:13] == 'postgresql://'
    except IOError:
        DBENGINE = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingDBServerFile(rel_dir(*DBFILE)))
        else:
            raise ctrlexception.MissingDBServerFile(rel_dir(*DBFILE))

    # get password if need be
    if DBENGINE.find(PASSTAG) != -1:
        _f = concat_dir(HOME, *PASSFILE)
        try:
            f = open(_f, mode='r')
            DBENGINE.replace(PASSTAG, f.readline().strip())
            f.close()
        except IOError:
            if NOERRORATIMPORT:
                print(ctrlexception.MissingDBPasswordFile(_f))
            else:
                raise ctrlexception.MissingDBPasswordFile(_f)

    # preparing the source callsign
    _f = concat_dir(HOME, *CSSOURCEFILE)
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
    _f = concat_dir(HOME, *CSDESTFILE)
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
    PACKETIDFULLFILE = concat_dir(HOME, *PACKETIDFILE)
    if not os.path.isfile(PACKETIDFULLFILE):
        PACKETIDFULLFILE = None
        if NOERRORATIMPORT:
            print(ctrlexception.MissingPacketIDFile(PACKETIDFULLFILE))
        else:
            raise ctrlexception.MissingPacketIDFile(PACKETIDFULLFILE)
