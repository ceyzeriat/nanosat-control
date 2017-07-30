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


from types import ModuleType
import sys
import glob
import os
import importlib

from . import generated


allparamfiles = ['generated']
for item in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
    dum = os.path.splitext(os.path.split(item)[1])[0]
    if dum == '__init__':
        continue
    allparamfiles.append(dum)


class module(ModuleType):
    """
    Automatically import objects from the modules
    """
    def __getattr__(self, name):
        if name in allparamfiles:
            module = importlib.import_module('param.{}'.format(name))
            setattr(self, name, module)
            return module
        return ModuleType.__getattribute__(self, name)

    def __dir__(self):
        """
        Just show what we want to show
        """
        result = list(new_module.__all__)
        result.extend(('__file__', '__path__', '__doc__', '__all__',
                       '__docformat__', '__name__', '__path__',
                       '__package__', '__version__'))
        return result

# keep a reference to this module so that it's not garbage collected
old_module = sys.modules['param']


# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules['param'] = module('param')
new_module.__dict__.update({
    '__file__':         __file__,
    '__package__':      'pld',
    '__path__':         __path__,
    '__doc__':          __doc__,
    '__all__':          tuple(allparamfiles),
    '__docformat__':    'restructuredtext en'
})
