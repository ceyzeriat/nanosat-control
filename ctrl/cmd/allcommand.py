#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from .command import Command
from . import param_commands
from ..utils import core


__all__ = ['ALLCMDS', 'L0CMDS', 'L1CMDS', 'ALLCMDSNAMES', 'L0CMDSNAMES',
			'L1CMDSNAMES']


f = open(core.rel_dir(*param_commands.COMMANDSFILE), mode='r')
allcmds = json.load(f)

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
