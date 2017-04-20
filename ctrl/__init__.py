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


import param
from . import utils
from . import ccsds
if not param.param_all.JUSTALIB:
    from . import cmd
    from . import db
    from . import c
    from . import c0
    from . import c1
    from . import cadcs
    if param.param_all.ENABLESHOW:
        from . import xdisp
from . import kiss
from ._version import __version__, __major__, __minor__, __micro__
if not param.param_all.JUSTALIB:
    from .telecommand import *
    from .telemetry import *
