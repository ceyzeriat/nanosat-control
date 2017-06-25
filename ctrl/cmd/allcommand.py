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


from param import param_commands

from .command import Command
from ..utils import core


# import all patches from patch-file
from .cmd_patch import *


__all__ = ['ALLCMDS', 'L0CMDS', 'L1CMDS', 'ALLCMDSNAMES', 'L0CMDSNAMES',
            'L1CMDSNAMES', 'L1OBCCMDS', 'L1OBCCMDSNAMES', 'L1PLDCMDS',
            'L1PLDCMDSNAMES']


allcmds = {}
for key, item in param_commands.COMMANDSFILE.items():
    if key != 'adcs':
        allcmds[key] = core.load_json_cmds(item)


ALLCMDS = []
L0CMDS = []
L1CMDS = []
L1OBCCMDS = []
L1PLDCMDS = []
ALLCMDSNAMES = []
L0CMDSNAMES = []
L1CMDSNAMES = []
L1OBCCMDSNAMES = []
L1PLDCMDSNAMES = []


for key, cmdfile in allcmds.items():
    for item in cmdfile:
        if item['name'] == 'set_datetime':
            c = setDatetime(**item)
        elif item['name'] in ['flash_read', 'flash_erase', 'flash_write', 'echo_bld', 'launch_application_A', 'launch_application_B', 'soft_reboot']:
            c = genericCrcPatch(**item)
        elif item['name'] == 'configure_rtc':
            c = configureRTC(**item)
        else:
            c = Command(**item)
            # dirty dirt to make auto-completion on commands
            params = ', '.join(["{}={}".format(n.name, n.name)\
                                                for n in c._params])
            lam_param = ', '.join([str(n.name) for n in c._params])
            exec('c.__call__ = lambda {}: c._wrapcall({})'\
                                        .format(lam_param, params))
        ALLCMDS.append(c)
        ALLCMDSNAMES.append(c.name)
        if c.level == 0:
            L0CMDS.append(c)
            L0CMDSNAMES.append(c)
        else:
            L1CMDS.append(c)
            L1CMDSNAMES.append(c)
            if c.payload == 0:
                L1OBCCMDS.append(c)
                L1OBCCMDSNAMES.append(c)
            else:
                L1PLDCMDS.append(c)
                L1PLDCMDSNAMES.append(c)
