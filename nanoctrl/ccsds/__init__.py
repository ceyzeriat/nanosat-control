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

from nanoutils.ccsds import ccsdsexception


from .ccsdsblob import CCSDSBlob
from .ccsdsunpacker import CCSDSUnPacker as _CCSDSUnPacker
from .ccsdspacker import CCSDSPacker as _CCSDSPacker


TCUnPacker = _CCSDSUnPacker(mode='tc')
TMUnPacker = _CCSDSUnPacker(mode='tm')
TMPacker = _CCSDSPacker(mode='tm')
TCPacker = _CCSDSPacker(mode='tc')
