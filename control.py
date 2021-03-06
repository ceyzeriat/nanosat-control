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

if __name__ == "__main__":
    import time
    from byt import Byt
    from nanoctrl import c
    from nanoctrl import c0
    from nanoctrl import c1
    from nanoctrl import co1
    from nanoctrl import cp1
    from nanoctrl import cadcs
    from nanoctrl import db
    from nanoctrl import Telemetry
    from nanoctrl import Telecommand
    from nanoutils import core
    from nanoutils import PosixUTC
    import nanoutils
    from nanoutils import bincore
    from nanoapps import controlling
    from nanoparam import param_all


    core.prepare_terminal('Control')
    print("Initialization...")
    controlling.init()
    if param_all.SAVETC:
        db.init_DB()
    else:
        print('DB not initialized')

    time.sleep(0.5)

    core.prepare_terminal('Control')
    print(param_all.ART)
