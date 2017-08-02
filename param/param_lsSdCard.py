#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 202-2017  Guillaume Schworer
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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O
from ctrl.utils.day import Day
from ctrl.utils.ms import Ms


__all__ = ['TROUSSEAU']


KEYS = [dict( name='file_name',
                                start=0*O,
                                l=8*O,
                                typ='text',
                                verbose="name of file on SD card (8 characters)",
                                disp="filename"),
		dict( name='file_ext',
                                start=8*O,
                                l=3*O,
                                typ='text',
                                verbose="extension of file on SD card (3 characters)",
                                disp="ext"),

        dict(  name='attribute',
                            start=11*O,
                            l=1*O,
                            typ='uint',
                            verbose="type of file",
                            disp="attr"),

        dict( name='timestamp',
                        start=12*O,
                        l=4*O,
                        typ='uint',
#                        fctfix=Day,
                        verbose='time of of the oldest Tm in the file in second after 1970',
                        disp="time"),

        dict( name='file_size',
                        start=16*O,
                        l=4*O,
                        typ='uint',
#                        fctfix=Ms,
                        verbose='size of the file',
                        disp="size")

        ]


TROUSSEAU = CCSDSTrousseau(KEYS, listof=True)
#TROUSSEAU = CCSDSTrousseau(KEYS)
