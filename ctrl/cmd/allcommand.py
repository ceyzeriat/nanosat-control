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


from .command import Command
from . import param_commands
from ..utils import core


__all__ = ['ALLCMDS', 'L0CMDS', 'L1CMDS', 'ALLCMDSNAMES', 'L0CMDSNAMES',
			'L1CMDSNAMES']


allcmds = core.load_json_cmds(param_commands.COMMANDSFILE)


ALLCMDS = []
L0CMDS = []
L1CMDS = []
ALLCMDSNAMES = []
L0CMDSNAMES = []
L1CMDSNAMES = []


for item in allcmds:
    c = Command(**item)
    ALLCMDS.append(c)
    ALLCMDSNAMES.append(c.name)
    if c.level == 0:
        L0CMDS.append(c)
        L0CMDSNAMES.append(c)
    else:
        L1CMDS.append(c)
        L1CMDSNAMES.append(c)