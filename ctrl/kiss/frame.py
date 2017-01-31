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


from . import utils
from . import constants
from ..utils import core
from .callsign import Callsign


__all__ = ['Framer']


class Frame(object):
    def __init__(self, source=None, destination=None, path=[]):
        """
        Codes/decodes a KISS frame
        """
        self.source = Callsign(core.str2bytes(source))\
                        if source is not None else b''
        self.destination = Callsign(core.str2bytes(destination))\
                            if destination is not None else b''
        self.path = list(map(Callsign, map(core.str2bytes, path)))\
                        if path != [] else []

    def reinit(self):
        self.source = Callsign(core.str2bytes(core.CSSOURCE))
        self.destination = Callsign(core.str2bytes(core.CSDESTINATION))
        self.path = []

    def encode_kiss(self, text):
        """
        Encodes an Frame as KISS.
        """
        self.text = core.str2bytes(text)
        enc_frame = self.destination.encode_kiss() +\
                        self.source.encode_kiss() +\
                        b''.join([path_call.encode_kiss()
                                    for path_call in self.path])
        frame = enc_frame[:-1] +\
                    core.ints2bytes(core.str2ints(enc_frame[-1])[0] | 0x01) +\
                    constants.SLOT_TIME +\
                    b'\xf0' +\
                    self.text
        frame = utils.escape_special_codes(frame)
        return constants.FEND + constants.DATA_FRAME + frame + constants.FEND

    def decode_kiss(self, frame):
        """
        Parses and Extracts the components of an KISS-Encoded Frame.
        """
        frame = utils.strip_df_start(frame)
        frameints = core.str2ints(frame)
        frame_len = len(frameints)
        if frame_len < 16:
            return None
        for idx, char in enumerate(frameints):
            # Is address field length correct?
            # Find the first ODD Byte followed by the next boundary:
            if (char & 0x01
                    and ((idx + 1) % 7) == 0):
                i = (idx + 1) / 7
                # Less than 2 callsigns?
                if 1 < i < 11:
                    # For frames <= 70 bytes
                    if frame_len >= idx + 2:
                        if (frameints[idx + 1] & 0x03 == 0x03 and
                                frameints[idx + 2] in [0xf0, 0xcf]):
                            text = frame[idx + 3:]
                            destination = Callsign(frame[:7])
                            source = Callsign(frame[7:])
                            #self._extract_kiss_path(frame, i)
                return source, destination, text


Framer = Frame(source=core.CSSOURCE, destination=core.CSDESTINATION)
