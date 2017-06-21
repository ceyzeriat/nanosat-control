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
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


MAXLENGTHERRORMESSAGE = 100


KEYS = [dict(   name='error_message',
                start=0,
                l=MAXLENGTHERRORMESSAGE,
                fctunpack=bincore.bin2hex,
                fctpack=bincore.hex2bin,
				verbose="Optional: an error message (ascii string). The message is only put in the frame if errorCode is not 0",
                disp='err')]


class EACKCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the execution acknowledgment

        Args:
        * data (byts): the chain of octets to unpack
        """
        data = Byt(data[:MAXLENGTHERRORMESSAGE])
        # optional error_message
        if len(data) == 0:
            return {self.keys[0].name: Byt()}
        return super(EACKCCSDSTrousseau, self).unpack(data)

    def disp(self, vals):
        """
        Display the trousseau values

        Args:
          * vals (dict): a dictionary containing the values to display
        """
        return "{}\nhex: {}".format(super(EACKCCSDSTrousseau, self).disp(vals),
                                    vals[self.keys[0].name].hex())


TROUSSEAU = EACKCCSDSTrousseau(KEYS, octets=True)
