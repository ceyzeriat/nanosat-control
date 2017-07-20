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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds.ccsdsmetatrousseau import CCSDSMetaTrousseau

from .generated.l0hkstructpart1 import L0HKSTRUCTPART1_KEYS
from .generated.l0hkstructpart2 import L0HKSTRUCTPART2_KEYS


__all__ = ['TROUSSEAU']


TROUSSEAUDICT = {0: CCSDSTrousseau(L0HKSTRUCTPART1_KEYS),
                 1: CCSDSTrousseau(L0HKSTRUCTPART2_KEYS)}


TROUSSEAU = CCSDSMetaTrousseau(TROUSSEAUDICT, key='hk_part')
