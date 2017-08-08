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


from byt import Byt


__all__ = ['escape_special_codes', 'valid_callsign', 'recover_special_codes',
            'strip_df_start']


# Marks START and END of a Frame
FEND = Byt('\xc0')

# Escapes FEND and FESC bytes within a frame
FESC = Byt('\xdb')

# Sent as FESC TFEND
TFEND = Byt('\xdc')

# Sent as FESC TFESC
TFESC = Byt('\xdd')

# 0xC0 is sent as 0xDB 0xDC
FESC_TFEND = FESC + TFEND

# 0xDB is sent as 0xDB 0xDD
FESC_TFESC = FESC + TFESC

# KISS Command Codes
DATA_FRAME = Byt('\x00')
SLOT_TIME = Byt('\x03')


def escape_special_codes(raw_codes):
    """
    Escape special codes, as per KISS specification

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    return raw_codes.replace(FESC, FESC_TFESC).replace(FEND, FESC_TFEND)


def valid_callsign(callsign):
    """
    Validates callsign and returns bool

    Args:
      * callsign (str): Callsign to validate
    """
    callsign = Byt(callsign).strip()
    # test for SSID
    if callsign.find(Byt('-')) != -1:
        if callsign.count(Byt('-')) == 1:
            callsign, ssid = callsign.split(Byt('-'))
        else:
            return False
    else:
        ssid = Byt('0')
    # Test length, call should be 2-6
    if not ((2 <= len(callsign) <= 6) and (1 <= len(ssid) <= 2)):
        return False
    # test for char content
    for char in callsign:
        if not (char.isalpha() or char.isdigit()):
            if not (char == Byt("*") and callsign[-1] == Byt("*")):
                return False
    # conversion in number fails
    if not ssid.isdigit():
        return False
    # SSID not in 0-15
    if not (0 <= int(ssid) <= 15):
        return False
    # finally
    return True


def strip_df_start(frame):
    """
    Strips KISS DATA_FRAME start (0x00) and newline from frame, and
    returns it

    Args:
      * frame: AX25 frame
    """
    if frame.startswith(FEND+DATA_FRAME):
        frame = frame[len(FEND+DATA_FRAME):]
    if frame.endswith(FEND):
        frame = frame[:-len(FEND)]
    return frame


def recover_special_codes(frame):
    """
    Recover special codes, as per KISS specification

    "If the FESC_TFESC or FESC_TFEND escaped codes appear in the data received,
    they need to be recovered to the original codes. The FESC_TFESC code is
    replaced by FESC code and FESC_TFEND is replaced by FEND code."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    res = Byt()
    iteration = iter(range(len(frame)))
    for idx in iteration:
        if frame[idx:idx+2] == FESC_TFEND:
            res += FEND
            next(iteration)
        elif frame[idx:idx+2] == FESC_TFESC:
            res += FESC
            next(iteration)
        else:
            res += frame[idx]
    return res

