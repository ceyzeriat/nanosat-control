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
import inflect
from ..utils import bincore
from ..utils import core


__all__ = ['CCSDSCategory']


class CCSDSCategory(object):
    def __init__(self, name, number, aux_trousseau=None,
                    data_file=None):
        """
        Defines a packet category

        Args:
          * name (str): the name of the category, for display. The
            right-most space-separated word shall be a singular noun
          * number (int): the id number of the category
          * aux_trousseau (None or Trousseau): None if the category
            has no auxiliary header, otherwise the Trousseau to unpack it
          * data_file (None or str): None if the category has no data
            field, or the name of the parameter file where its trousseau
            is defined
        """
        self.name = str(name)
        self.table_name = core.clean_name(str(name).replace(' ', '_')).lower()
        inf = inflect.engine()
        if inf.singular_noun(self.table_name) is False:
            self.table_name = inf.plural_noun(self.table_name)
        self.object_name = core.camelize_singular(self.table_name)
        self.number = int(number)
        self.bits = bincore.int2bin(self.number, pad=5)
        self.aux_trousseau = aux_trousseau
        self.aux_size = getattr(self.aux_trousseau, 'size', 0)
        if self.aux_trousseau is None:
            self.table_aux_name = None
            self.object_aux_name = None
        else:
            self.table_aux_name = "tmcat_" + self.table_name
            self.object_aux_name = core.camelize_singular(self.table_aux_name)
        self.data_file = data_file if data_file is None else str(data_file)
        if self.data_file is None:
            self.table_data_name = None
            self.object_data_name = None
        else:
            self.table_data_name = "data_" + self.table_name
            self.object_data_name = core.camelize_singular(self.table_data_name)
