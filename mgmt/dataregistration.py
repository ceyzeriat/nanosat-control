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
from ctrl.utils import core as ctrlcore

from . import mgmtexception
from .registration import Registration


__all__ = ['DataRegistration']


class DataRegistration(Registration):
    def __init__(self, param_file, table_name):
        """
        Registers a new TM data-category into the database

        Args:
          * param_file (str): the param file name containing the
            ccsds keys Trousseau
          * table_name (str): the name of the table, lower-case
            underscored plural, e.g. 'the_aliens'
        """
        if not hasattr(param, str(param_file)):
            print("No such file parameter '{}'".format(param_file))
            return
        self.cat = getattr(param, str(param_file)).TROUSSEAU
        if table_name[:5] != 'data_':
            table_name = 'data_' + table_name
        cat_name = ctrlcore.camelize_singular(str(table_name))
        if cat_name is False:
            print('The name provided is not a valid lower-case underscored '\
                  'plural')
            return
        self.cat_name = cat_name
        super(DataRegistration, self).__init__()
