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


from .cm import Cm
from .cmadcs import CmADCS
from .command import Command


__all__ = ['CommandADCS']


class CommandADCS(CmADCS, Command):
    def __init__(self, *args, **kwargs):
        """
        Sends the command and stores it in the database

        Args ar ignored

        Kwargs:
          * the input parameters of the command
          * rack (bool): ``True`` to get the acknowledgement of reception
          * fack (bool): ``True`` to get the acknowledgement of format
          * eack (bool): ``True`` to get the acknowledgement of execution
          * signit (bool): ``True`` to sign the telecommand
          * wait (bool): ``True`` to make a blocking telecommand, until
            the acknowledgement is received, or ``timetout`` is elapsed
          * timeout (int): the time in second to wait for acknowledgements
        """
        # sole purpose of this __init__ is overwrite the docstring
        super(CommandADCS, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.send(**kwargs)
