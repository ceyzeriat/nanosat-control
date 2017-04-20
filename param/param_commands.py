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


MINLENPARAMSTRUCTURE = 3

COMMANDSFILE = {'obc0': ["ctrl", "cmd", "cmds_obc0.json"],
				'obc1': ["ctrl", "cmd", "cmds_obc1.json"],
				'pld0': ["ctrl", "cmd", "cmds_pld0.json"],
				'pld1': ["ctrl", "cmd", "cmds_pld1.json"],
				'adcs': ["ctrl", "cmd", "cmds_adcs.json"],}


RANGESEPARATOR = '_'

LISTSEPARATOR = '!'

LENPARAMNAME = 25


CSVSUBSYSTEM = 0
CSVNUMBER = 1
CSVNAME = 2
CSVSUBSYSTEMKEYADCS = 3
CSVCOMMANDIDADCS = 4
CSVPID = 6
CSVDESC = 7
CSVLPARAM = 14
CSVNPARAM = 15

CSVPARAMDESC = 16
CSVPARAMNAME = 17
CSVPARAMTYP = 18
CSVPARAMSIZE = 19
CSVPARAMUNIT = 20
CSVPARAMRNG = 21

