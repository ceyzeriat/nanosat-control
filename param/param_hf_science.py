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


__all__ = ['TROUSSEAU']


KEYS = [dict(   name='step',
                start=0*O,
                l=1*O,
                typ='uint',
                verbose="step",
                disp="step"),

        dict(   name='counts',
                start=1*O,
                l=4*O,
                typ='uint',
                verbose="counts",
                disp="cts"),

        dict(   name='x_com',
                start=5*O,
                l=2*O,
                typ='uint',
                verbose="x_com",
                disp="xc"),

        dict(   name='y_com',
                start=7*O,
                l=2*O,
                typ='uint',
                verbose="y_com",
                disp="yc"),

        dict(   name='x_pos',
                start=9*O,
                l=2*O,
                typ='uint',
                verbose="x_pos",
                disp="xp"),

        dict(   name='y_pos',
                start=11*O,
                l=2*O,
                typ='uint',
                verbose="y_pos",
                disp="yp")
        ]


TROUSSEAU = CCSDSTrousseau(KEYS, listof=True)
