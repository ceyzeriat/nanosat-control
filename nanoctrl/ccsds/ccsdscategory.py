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
from param import param_category
import inflect


from . import ccsdsexception as exc
from ..utils import bincore
from ..utils import core
from ..ccsds.ccsdsmetatrousseau import CCSDSMetaTrousseau


__all__ = ['CCSDSCategory']


class CCSDSCategory(object):
    def __init__(self, name, number, aux_trousseau=None, verbose='',
                    data_file=None, thatsTCANS=False):
        """
        Defines a packet category

        Args:
          * name (str): the name of the category, for display. The
            right-most space-separated word shall be a singular noun
          * number (int): the id number of the category
          * aux_trousseau (None or Trousseau): None if the category
            has no auxiliary header, otherwise the Trousseau to unpack it
          * verbose (str): some more details
          * data_file (None or str): None if the category has no data
            field, or the name of the parameter file where its trousseau
            is defined
        """
        # deal with name checking
        if name != core.clean_name(name, allow_space=True):
            raise exc.WrongNameFormat(name)
        self.name = str(name)
        self.verbose = str(verbose)
        self._thatsTCANS = bool(thatsTCANS)
        self.table_name = core.clean_name(self.name.replace(' ', '_')).lower()
        inf = inflect.engine()
        if inf.singular_noun(self.table_name) is False:
            self.table_name = inf.plural_noun(self.table_name)
            if self.table_name is False:
                raise exc.WrongCategoryTableName(self.table_name)
        self.object_name = core.camelize_singular(self.table_name)
        if self.object_name is False:
            raise exc.WrongCategoryObjectName(self.object_name)
        if self.table_name != core.camelize_singular_rev(self.object_name):
            raise exc.WrongCategoryTableName(self.table_name)
        # name was satisfactory, doing other stuff
        self.number = int(number)
        self.bits = bincore.int2bin(self.number, pad=5)
        # AUX HEADER STUFF
        self.aux_trousseau = aux_trousseau
        self.aux_size = getattr(self.aux_trousseau, 'size', 0)
        if self.aux_trousseau is None:
            self.table_aux_name = None
        else:
            self.table_aux_name = "tmcat_" + self.table_name
        # DATA FIELD STUFF
        self.data_file = None if data_file is None else str(data_file)
        if self.data_file is None:
            self._table_data_name = None
            self._table_data_conv_name = None
            self.data_trousseau = None
            self.is_data_metatr = False
        else:
            self.data_trousseau = getattr(param, self.data_file).TROUSSEAU
            self.is_data_metatr = isinstance(self.data_trousseau,
                                             CCSDSMetaTrousseau)
            # if not metatrousseau
            if not self.is_data_metatr:
                self._table_data_name = "data_" + self.table_name
                # if no conversion
                if not self.data_trousseau.unram_any:
                    self._table_data_conv_name = None
                else:  # if at least 1 conversion
                    self._table_data_conv_name =\
                        self._table_data_name + '_values'
            elif self._thatsTCANS:  # TC ANS special case
                self._table_data_name = "data_" + self.table_name
                self._table_data_conv_name = None
            else:  # if metatrousseau
                self._table_data_name = {}
                self._table_data_conv_name = {}
                for trkey, tr in self.data_trousseau.TROUSSEAUDIC.items():
                    self._table_data_name[trkey] = "data_p{}_{}"\
                                        .format(trkey, self.table_name)
                    if not tr.unram_any:
                        self._table_data_conv_name[trkey] = None
                    else:  # if at least 1 conversion
                        self._table_data_conv_name[trkey] =\
                                    self._table_data_name[trkey] + '_values'

    def get_table_data_name(self, hdx, *args, **kwargs):
        if self._table_data_name is None:
            return None
        elif not self.is_data_metatr or self._thatsTCANS:
            return self._table_data_name
        elif hdx.get(self.data_trousseau.key) in\
                                    self._table_data_name.keys():
            return self._table_data_name[hdx.get(self.data_trousseau.key)]
        else:
            raise exc.InvalidMetaTrousseauKey(hdx.get(self.data_trousseau.key))

    def get_table_data_conv_name(self, hdx, *args, **kwargs):
        if self._table_data_conv_name is None:
            return None
        elif not self.is_data_metatr:
            return self._table_data_conv_name
        elif hdx.get(self.data_trousseau.key) in\
                                    self._table_data_conv_name.keys():
            return self._table_data_conv_name[hdx.get(self.data_trousseau.key)]
        else:
            raise exc.InvalidMetaTrousseauKey(hdx.get(self.data_trousseau.key))

    def get_trousseau_keys(self, hdx, *args, **kwargs):
        if self.data_trousseau is None:
            return []
        elif not self.is_data_metatr:
            return self.data_trousseau.keys
        elif hdx.get(self.data_trousseau.key) in\
                                    self._table_data_conv_name.keys():
            return self.data_trousseau.TROUSSEAUDIC[\
                                        hdx.get(self.data_trousseau.key)].keys
        else:
            raise exc.InvalidMetaTrousseauKey(hdx.get(self.data_trousseau.key))
