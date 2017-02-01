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


import time
from ctrl.utils import core
from ctrl import listening
from ctrl import db


print("Initialization...")
listening.init_listening(antenna=core.ANTENNALISTENED)
db.init_DB()

print("Starting...")
while 1:
    #time.sleep(1./core.ANTENNARPORTREADFREQ)
    n = listening.ANTENNA.in_waiting()
    if n > 0:
        # grab data
        data = listening.ANTENNA.read(size=n)
        if data != '':
            # deal with it in a separate thread
            loopy = Thread(target=listening.process_data, args=(data, ))
            loopy.daemon = True
            loopy.start()

"""
        Reads data from KISS device.

        :param callback: Callback to call with decoded data.
        :param readmode: If False, immediately returns frames.
        :type callback: func
        :type readmode: bool
        :return: List of frames (if readmode=False).
        :rtype: list
        
        read_buffer = b''

        read_bytes = read_bytes or kiss.READ_BYTES
        
        while 1:
            read_data = self.interface.recv(read_bytes)
            if read_data == b'':
                raise Exception('Socket Closed')

            if read_data is not None and len(read_data):
                frames = []

                split_data = read_data.split(kiss.FEND)
                len_fend = len(split_data)
                # Handle NMEAPASS on T3-Micro
                if len(read_data) >= 900:
                    if kiss.NMEA_HEADER in read_data and '\r\n' in read_data:
                        if callback:
                            callback(read_data)
                        elif not readmode:
                            return [read_data]

                # No FEND in frame
                if len_fend == 1:
                    read_buffer = ''.join([read_buffer, split_data[0]])
                # Single FEND in frame
                elif len_fend == 2:
                    # Closing FEND found
                    if split_data[0]:
                        # Partial frame continued, otherwise drop
                        frames.append(b''.join([read_buffer, split_data[0]]))
                        read_buffer = b''
                    # Opening FEND found
                    else:
                        frames.append(read_buffer)
                        read_buffer = split_data[1]
                # At least one complete frame received
                elif len_fend >= 3:
                    # Iterate through split_data and extract just the frames.
                    for i in range(0, len_fend - 1):
                        _str = b''.join([read_buffer, split_data[i]])
                        if _str:
                            frames.append(_str)
                            read_buffer = b''
                    if split_data[len_fend - 1]:
                        read_buffer = split_data[len_fend - 1]

                # Fixup T3-Micro NMEA Sentences
                frames = map(kiss.strip_nmea, frames)

                # Remove None frames.
                frames = filter(None, frames)

                # Maybe.
                frames = map(kiss.recover_special_codes, frames)

                if self.strip_df_start:
                    frames = map(kiss.strip_df_start, frames)

                if readmode:
                    for frame in frames:
                        callback(frame)
                elif not readmode:
                    return frames
"""
