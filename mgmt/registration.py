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


from ctrl.utils import core


__all__ = ['Registration']


class Registration(object):
    def __init__(self):
        decam = core.camelize_singular_rev(self.cat_name)
        if decam is False:
            print("The name '{}' is not a valid decamelized "\
                  "plural".format(self.cat_name))
            return
        recam = core.camelize_singular(decam)
        if recam is False or recam != self.cat_name:
            print("The name '{}' is not reversely plural-camelize-able. You "\
                  "killed a camel and you should be ashamed"\
                  .format(self.cat_name))
            return
        self.table_name = decam

    def delete_table(self):
        """
        Provides postgresql code to delete the table
        """
        print("DROP TABLE {} CASCADE;".format(self.table_name))
        print("If this table contains data, deleting it will delete all data"\
              "contained in it and may corrupt other data referring to it. "\
              "Use at your own risk.")

    def show(self):
        """
        Show the content of the category
        """
        print("Category '{}', DB Table '{}'\n".format(self.cat_name,
                                                      self.table_name))
        for item in self.cat.keys:
            print(item)
            if item.name != item.name.lower():
                print('!!! uppercase is not allowed in ccsds keys')

    def create_table(self):
        """
        Provides postgresql code to create the table
        """
        query = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    id serial PRIMARY KEY,
    telemetry_packet integer UNIQUE{fields}
);
ALTER TABLE {table_name} OWNER TO picsat_admin;
GRANT ALL ON {table_name} TO picsat_admin;
GRANT select ON {table_name} TO picsat_read;
GRANT select, insert, update ON {table_name} TO picsat_edit;
ALTER TABLE {table_name} ADD FOREIGN KEY (telemetry_packet) REFERENCES telemetries (id);
GRANT ALL ON SEQUENCE {table_name}_id_seq TO picsat_edit;
        """
        types_conv = {'2bool': 'boolean',
                      '2intSign': [16, 'smallint', 'integer'],
                      '2int': [15, 'smallint', 'integer'],
                      '2hex': 'bytea',
                      '2txt': [125, 'varchar({len})', 'text'],
                      '2float': [32, 'real', 'double precision']}
        fields = ""
        for item in self.cat.keys:
            for k, v in types_conv.items():
                if item._fctunpack.__name__.find(k) != -1:
                    if isinstance(v, list):
                        v = v[1] if item.len <= v[0] else v[2]
                    break
            else:
                v = '?TYPE?'
            fields += ',\n    {} {}'.format(item.name, str(v).format(len=item.len))
        print(query.format(table_name=self.table_name, fields=fields))
