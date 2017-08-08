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
from nanoparam import param_all_processed as param_all


from . import kissutils
from .callsign import Callsign


__all__ = ['Framer']


class Frame(object):
    def __init__(self, source=None, destination=None, path=[],
                    kiss=None):
        """
        Codes/decodes an AX25+KISS frame

        Args:
          * source, destination (str): the callsigns
          * path: unused
          * kiss (bool): whether the frames are AX25, or KISS+AX25
        """
        self.ISKISS = bool(kiss) if kiss is not None else param_all.KISSENCAPS
        self.reinit(source=source, destination=destination, path=path)

    def reinit(self, source=None, destination=None, path=[]):
        self.source = Callsign(source) if source is not None\
                        else Callsign('')
        self.destination = Callsign(destination) if destination is not None\
                        else Callsign('')
        self.path = list(map(Callsign, path)) if path != [] else []

    def encode_radio(self, text):
        """
        Encodes an Frame as AX25+KISS
        """
        self.text = Byt(text)
        enc_frame = self.destination.encode_callsign() +\
                        self.source.encode_callsign() +\
                        Byt().join([path_call.encode_callsign()
                                    for path_call in self.path])
        frame = enc_frame[:-1] +\
                    Byt(ord(enc_frame[-1]) | 0x01) +\
                    kissutils.SLOT_TIME +\
                    Byt('\xf0') +\
                    self.text
        if not self.ISKISS:
            return frame
        else:
            frame = kissutils.escape_special_codes(frame)
            return kissutils.FEND + kissutils.DATA_FRAME + frame\
                      + kissutils.FEND

    def decode_radio(self, frame):
        """
        Parses and extracts the components of an AX25+KISS-Encoded Frame
        """
        # init
        source, destination, text = Byt(), Byt(), Byt()
        if self.ISKISS:
            # parse KISS away
            frame = kissutils.strip_df_start(frame)
            # recover special codes
            frame = kissutils.recover_special_codes(frame)
        frameints = frame.ints()
        frame_len = len(frameints)
        if frame_len > 16:
            for idx, char in enumerate(frameints):
                # Is address field length correct?
                # Find the first ODD Byte followed by the next boundary:
                if (char & 0x01 and ((idx + 1) % 7) == 0):
                    i = (idx + 1) // 7
                    # Less than 2 callsigns? For frames <= 70 bytes
                    if 1 < i < 11 and frame_len >= idx + 2:
                        if (frameints[idx + 1] & 0x03 == 0x03 and
                                frameints[idx + 2] in [0xf0, 0xcf]):
                            text = frame[idx + 3:]
                            destination = Callsign(frame[:7])
                            source = Callsign(frame[7:])
                            #self._extract_kiss_path(frame, i)
                    return source, destination, text
        return source, destination, text


Framer = Frame(source=param_all.CSSOURCE, destination=param_all.CSDESTINATION)

