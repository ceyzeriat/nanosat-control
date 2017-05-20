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


from param import param_category

from . import mgmtexception
from .registration import Registration


__all__ = ['CategoryRegistration']


class CategoryRegistration(Registration):
    def __init__(self, pld_flag, cat_num):
        """
        Registers a new TM category into the database

        Args:
          * pld_flag (int): payload flag, 0 or 1
          * cat_num (int): category number
        """
        self.pld_flag = int(pld_flag)
        self.cat_num = int(cat_num)
        self.cat = param_category.CATEGORIES[self.pld_flag][self.cat_num]
        self.cat_name = self.cat.table_name
        super(CategoryRegistration, self).__init__()
