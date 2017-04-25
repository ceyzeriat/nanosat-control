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


#import csv
#from param import param_all
#from param import param_apid
#from param import param_commands

from . import core
from . import mgmtexception


class CategoryRegistration(object):
    def __init__(self, pld_flag, cat_num, ):
        """
        Manages the list of commands.

        Args:
          * pld_flag (int): payload flag, 0 or 1
          * cat_num (int): category number
        """
        self.pld_flag = int(pld_flag)
        self.cat_num = int(cat_num)
        self.keys = PACKETCATEGORIES[self.pld_flag][self.cat_num]
        self.table_name = TABLECATEGORY[self.pld_flag][self.cat_num]
        decam = core.camelize_singular_rev(self.table_name)
        if decam is False:
            print("The name '{}' is not a valid camelized "\
                  "plural".format(self.table_name))
            return
        recam = core.camelize_singular(decam)
        if recam is False or recam != self.table_name:
            print("The name '{}' is not reversely camelize-able. You killed "\
                  "a camel and you should be ashamed".format(self.table_name))
            return
        self.table_name_decam = decam

    def delete_table(self):
        """
        Provides postgresql code to delete the table
        """
        print("DROP TABLE {} CASCADE;".format(self.table_name_decam))
        print("If this table contains data, deleting it will delete all data"\
              "contained in it and may corrupt other data referring to it. "\
              "Use at your own risk.")




CREATE TABLE IF NOT EXISTS tmcat_payload_hks
(
	id 					serial PRIMARY KEY,
	telemetry_packet	integer UNIQUE
);
ALTER TABLE tmcat_payload_hks OWNER TO picsat_admin;
GRANT ALL ON tmcat_payload_hks TO picsat_admin;
GRANT select ON tmcat_payload_hks TO picsat_read;
GRANT select, insert, update ON tmcat_payload_hks TO picsat_edit;
CREATE INDEX ON tmcat_payload_hks(telemetry_packet);
ALTER TABLE tmcat_payload_hks ADD FOREIGN KEY (telemetry_packet) REFERENCES telemetries (id);
GRANT ALL ON SEQUENCE tmcat_payload_hks_id_seq TO picsat_edit;