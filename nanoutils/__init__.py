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


import os
import sys
PYTHON3 = sys.version_info > (3,)


from . import ctrlexception
from . import bincore
from .bindiff import Bindiff
from .ms import Ms
from . import param_sys
from .pidwatchdog import PIDWatchDog
from .posixutc import PosixUTC
from .report import REPORTS, REPORTSDATA, EXTRADISPKEY
from .unit import O, b

if os.path.exists(os.path.join(__file__, 'hmac', param_sys.HMACLIBLINUX)):
    from .hmac import hmac


from .day import Day
from . import core
from . import ccsds
