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
import json
from byt import Byt
from nanoparam import param_all_processed as param_all


from .fcts import *
from . import fcts as _fcts
from . import ctrlexception as exc
from .posixutc import PosixUTC


def get_tc_packet_id():
    """
    Just reads the packet id from the file
    """
    f = open(param_all.PACKETIDFULLFILE.path, mode='r')
    res = int(f.readline().strip())
    f.close()
    return res


def get_next_tc_packet_id():
    """
    Reads the packet id from the file and adds one
    """
    return (get_tc_packet_id()+1) % param_all.MAXPACKETID


def get_set_next_tc_packet_id():
    """
    Reads the packet id from the file, adds one and saves new value
    """
    v = get_next_tc_packet_id()
    f = open(param_all.PACKETIDFULLFILE.path, mode='w')
    f.write(str(v))
    f.close()
    return v


def append_logfile(message):
    """
    Appends message at the end of the log file, with a timestamp

    Args:
      * message (str): the message to append
    """
    f = open(param_all.LOGFILE.path, mode="a")
    f.write('{} {}\n'\
                .format(_fcts.now().strftime(param_all.LOGFILETIMESTAMPFMT),
                        str(message)))
    f.close()


def recover_ccsds(data):
    """
    Recovers the un-escaped split characters

    Args:
      * data (str or list of str): the text to process
    """
    return data.replace(param_all.CCSDSESCAPEDSPLIT, param_all.CCSDSSPLITCHAR)


def split_ccsds(data, n):
    """
    Splits the ccsds according to the defined split ccsds character.
    Returns a list of size 1 at minimum, and ``n+1`` at maximum, which
    [-1] element is the remainder of the operation
    
    Args:
      * data (Byt): the bytes-chain to split
      * n (int): the maximum number of packets to split
    """
    return data.split(param_all.CCSDSSPLITCHAR*2, n)


def split_flow(data, n=-1):
    """
    Splits packets from flow if flow mode activated

    Args:
      * data (Byt): the data flow to split
      * n (int): how many packets should be splited, at maximum,
        set to -1 for all
    """
    if not param_all.FRAMESFLOW:
        raise exc.NotInFramesFlow()
    # split CCSDS using the special split chars
    if not AX25ENCAPS:
        res = split_ccsds(Byt(data), int(n))
        # no split found
        if len(res) < 2:
            return res
        # apply recovery of escaped chars to all splits found except last one
        return list(map(recover_ccsds, res[:-1])) + res[-1:]
    # split KISS using the special split chars
    elif param_all.KISSENCAPS:
        raise exc.NotImplemented("Frames-FLow with KISS")
    else:
        raise exc.NotImplemented("Unknown mode")


def merge_flow(datalist, trailingSplit=True):
    """
    Merges the packets if the flow mode is activated

    Args:
    * datalist (list of Byt): the packets to merge together
    * trailingSplit (bool): whether to add a trailing split character
    """
    if not param_all.FRAMESFLOW:
        raise exc.NotInFramesFlow()
    # merge CCSDS using the special split chars
    if not param_all.AX25ENCAPS:
        res = (param_all.CCSDSSPLITCHAR*2).join([
                    Byt(item).replace(param_all.CCSDSSPLITCHAR,
                                      param_all.CCSDSESCAPEDSPLIT)\
                        for item in datalist\
                            if len(item) > 0])
        if trailingSplit:
            res += param_all.CCSDSSPLITCHAR*2
        return res
    # merge KISS using the special split chars
    elif param_all.KISSENCAPS:
        raise exc.NotImplemented("Frames-FLow with KISS")
    else:
        raise exc.NotImplemented("Unknown mode")


def load_json_cmds(path):
    """
    Loads all the commands from the json file, given the path list
    """
    f = open(param_all.Pathing('param', *path).path, mode='r')
    allcmds = json.load(f)
    f.close()
    return allcmds


def packetfilename2datetime(txt):
    """
    Give a filename following `TELEMETRYNAMEFORMAT`
    """
    txt = os.path.basename(txt)
    dd, ms = txt.split('_')[1:]
    dd, tt = dd.split('T')
    dt = [int(dd[:4]), int(dd[4:6]), int(dd[6:])]
    dt = dt + [int(tt[:2]), int(tt[2:4]), int(tt[4:])]
    dt += [int(ms.split('.')[0])]
    return PosixUTC(*dt)


def now2daystamp():
    """
    Returns a day stamp for datetime t
    """
    return time2daystamp(_fcts.now())


def now2msstamp():
    """
    Returns a milli-sec stamp for now
    """
    return time2msstamp(_fcts.now())


def time2msstamp(t):
    """
    Returns a milli-sec stamp for datetime t
    """
    return int(t.hour * 36e5 + t.minute * 6e4 + t.second * 1e3
                + t.microsecond//1000)


def time2daystamp(t):
    """
    Returns a day stamp for now, or from t (PosixUTC)
    """
    return int(t.totimestamp()/86400.-param_all.DATETIME_REF)


def time2stamps(dt):
    """
    Give a PosixUTC, get ms and day stamps
    """
    return (time2msstamp(dt), time2daystamp(dt))


def stamps2time(daystamp, msstamp):
    """
    Give a day and a milli-sec stamp, return a datetime
    """
    ts = (param_all.DATETIME_REF+daystamp)*86400. + msstamp*0.001
    return PosixUTC.fromtimestamp(ts)
