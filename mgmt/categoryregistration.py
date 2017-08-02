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


__all__ = ['CategoryRegistration']


QUERY = """
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

QUERYCONV = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    id serial PRIMARY KEY,
    rawdata_id integer{fields}
);
ALTER TABLE {table_name} OWNER TO picsat_admin;
GRANT ALL ON {table_name} TO picsat_admin;
GRANT select ON {table_name} TO picsat_read;
GRANT select, insert, update ON {table_name} TO picsat_edit;
ALTER TABLE {table_name} ADD FOREIGN KEY (rawdata_id) REFERENCES {table_daddy_name} (id);
GRANT ALL ON SEQUENCE {table_name}_id_seq TO picsat_edit;
"""

# syntax: 'type tag in function': 'sql type'
# or 'type tag in function': [len limit (int),
#                             'sql type if len <= than len limit',
#                             'sql type if len > than len limit']
TYPESCONV = { '2bool': 'boolean',
              '2intSign': ['smallint', 16, 'integer', 32, 'bigint'],
              '2int': ['smallint', 15, 'integer', 31, 'bigint'],
              '2hex': 'bytea',
              '2txt': ['varchar({len})', 125, 'text'],
              '2float': 'real',
              '2double': 'double precision'}


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
        return base_create_table(self.cat)


def base_create_table(cat):
    ret = []
    # HEADER AUX
    if cat.aux_trousseau is not None:
        fields = ""
        for item in cat.aux_trousseau.keys:
            v = get_type_right(item)
            fields += ',\n    {} {}'.format(item.name,
                                            str(v).format(len=item.len))
        ret.append(QUERY.format(table_name=cat.table_aux_name,
                                unique=" UNIQUE",
                                fields=fields))
    # DATA FIELD
    if cat.data_trousseau is None:
        return "\n\n".join(ret)
    if not cat.is_data_metatr:
        fields = ""
        for item in cat.data_trousseau.keys:
            v = get_type_right(item)
            fields += ',\n    {} {}'.format(item.name,
                                            str(v).format(len=item.len))
        ret.append(QUERY.format(table_name=cat.get_table_data_name({}),
                                unique="",
                                fields=fields))
        # a conversion table
        if cat.data_trousseau.unram_any:
            fields = ""
            for item in cat.data_trousseau.keys:
                if item.unram is None:
                    continue
                fields += ',\n    {} real'.format(item.name)
            ret.append(QUERYCONV.format(
                        table_name=cat.get_table_data_conv_name({}),
                        table_daddy_name=cat.get_table_data_name({}),
                        fields=fields))
    else:
        metakey = cat.data_trousseau.key
        for trkey, tr in cat.data_trousseau.TROUSSEAUDIC.items():
            fields = ""
            for item in tr.keys:
                v = get_type_right(item)
                fields += ',\n    {} {}'.format(item.name,
                                                str(v).format(len=item.len))
            ret.append(QUERY.format(
                        table_name=cat.get_table_data_name({metakey: trkey}),
                        unique="",
                        fields=fields))
            # a conversion table
            if tr.unram_any:
                fields = ""
                for item in tr.keys:
                    if item.unram is None:
                        continue
                    fields += ',\n    {} real'.format(item.name)
                ret.append(QUERYCONV.format(
                            table_name=cat.get_table_data_conv_name(\
                                                            {metakey: trkey}),
                            table_daddy_name=cat.get_table_data_name(\
                                                            {metakey: trkey}),
                            fields=fields))
    return "\n\n".join(ret)



def get_type_right(item):
    for k, v in TYPESCONV.items():
        if item._fctunpack.__name__.endswith(k):
            if isinstance(v, list):
                if item.len <= v[1]:
                    v = v[0]
                else:
                    if len(v) == 5:
                        if item.len <= v[3]:
                            v = v[2]
                        else:
                            v = v[4]
                    else:
                        v = v[2]
            break
    else:
        raise Exception("unknown unpack function: {}"\
                            .format(item._fctunpack.__name__))
    return v