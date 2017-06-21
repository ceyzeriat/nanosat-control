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
from ctrl.utils import core
from ctrl.ccsds import CCSDSTrousseau

from . import mgmtexception


__all__ = ['CategoryRegistration', 'base_create_table']


class CategoryRegistration(object):
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

    def delete_table(self):
        """
        Provides postgresql code to delete the table
        """
        theresone = False
        if self.cat.table_aux_name is not None:
            print("DROP TABLE {} CASCADE;".format(self.cat.table_aux_name))
            theresone = True
        # if meta-trousseau, skip. It is managed manually
        if self.cat.table_data_name is not None and\
                isinstance(self.cat.data_trousseau, CCSDSTrousseau):
            print("DROP TABLE {} CASCADE;".format(self.cat.table_data_name))
            theresone = True
            if not theresone:
                print('No table associated to this category.')
            else:
                print("If this table contains data, deleting it will delete "\
                      "all data contained in it and may corrupt other data "\
                      "referring to it. Use at your own risk.")

    def show(self):
        """
        Shows the content of the category
        """
        # AUX HEADER
        if self.cat.table_aux_name is not None:
            print("\n\nCategory '{}', Auxiliary Header Table '{}'\n".format(
                                                self.cat.name,
                                                self.cat.table_aux_name))
            for item in self.cat.aux_trousseau.keys:
                print(item)
                if item.name != item.name.lower():
                    print('!!! uppercase is not allowed in ccsds keys')
        # DATA FIELD
        if self.cat.table_data_name is not None and\
                isinstance(self.cat.data_trousseau, CCSDSTrousseau):
            print("\n\nCategory '{}', Data field Table '{}'\n".format(
                                                self.cat.name,
                                                self.cat.table_data_name))
            for item in self.cat.data_trousseau.keys:
                print(item)
                if item.name != item.name.lower():
                    print('!!! uppercase is not allowed in ccsds keys')

    def create_table(self):
        """
        Provides postgresql code to create the table
        """
        return base_create_table(self.cat.aux_trousseau,\
                                 self.cat.table_aux_name,\
                                 self.cat.data_trousseau,\
                                 self.cat.table_data_name)


def base_create_table(aux_trousseau, table_aux_name, data_trousseau,\
                        table_data_name):
    query = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    id serial PRIMARY KEY,
    telemetry_packet integer{unique}{fields}
);
ALTER TABLE {table_name} OWNER TO picsat_admin;
GRANT ALL ON {table_name} TO picsat_admin;
GRANT select ON {table_name} TO picsat_read;
GRANT select, insert, update ON {table_name} TO picsat_edit;
ALTER TABLE {table_name} ADD FOREIGN KEY (telemetry_packet) REFERENCES telemetries (id);
GRANT ALL ON SEQUENCE {table_name}_id_seq TO picsat_edit;
    """
    # syntax: 'type tag in function': 'sql type'
    # or 'type tag in function': [len limit (int),
    #                             'sql type if len <= than len limit',
    #                             'sql type if len > than len limit']
    types_conv = {'2bool': 'boolean',
                  '2intSign': [16, 'smallint', 'integer'],
                  '2int': [15, 'smallint', 'integer'],
                  '2hex': 'bytea',
                  '2txt': [125, 'varchar({len})', 'text'],
                  '2float': [32, 'real', 'double precision']}
    ret = []
    # HEADER AUX
    if aux_trousseau is not None:
        fields = ""
        conv = 8 if aux_trousseau.octets else 1
        for item in aux_trousseau.keys:
            for k, v in types_conv.items():
                if item._fctunpack.__name__.endswith(k):
                    if isinstance(v, list):
                        v = v[1] if item.len*conv <= v[0] else v[2]
                    break
            else:
                v = '?TYPE?'
            fields += ',\n    {} {}'.format(item.name,
                                            str(v).format(len=item.len))
        ret.append(query.format(table_name=table_aux_name,
                                unique=" UNIQUE",
                                fields=fields))
    # DATA FIELD
    if data_trousseau is not None and\
            isinstance(data_trousseau, CCSDSTrousseau):
        fields = ""
        conv = 8 if data_trousseau.octets else 1
        for item in data_trousseau.keys:
            for k, v in types_conv.items():
                if item._fctunpack.__name__.endswith(k):
                    if isinstance(v, list):
                        v = v[1] if item.len*conv <= v[0] else v[2]
                    break
            else:
                v = '?TYPE?'
            fields += ',\n    {} {}'.format(item.name,
                                            str(v).format(len=item.len))
        ret.append(query.format(table_name=table_data_name,
                                unique="",
                                fields=fields))
    return "\n\n".join(ret)
