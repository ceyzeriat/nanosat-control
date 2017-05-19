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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore

from . import param_category_obc as obc
from . import param_category_pld as pld


# shape of all this stuff is
# DICTIONNARY[payload_flag(int)][packet_category(int)]

CATEGORYREGISTRATION = [{}, {}]
PACKETCATEGORIES = [{}, {}]
PACKETCATEGORYSIZES = [{}, {}]
TABLECATEGORY = [{}, {}]
TABLEDATA = [{}, {}]
FILEDATACRUNCHING = [{}, {}]


# grab the OBC dictionnaries
for k in obc.CATEGORYREGISTRATIONOBC.keys():
    CATEGORYREGISTRATION[0][k] = obc.CATEGORYREGISTRATIONOBC[k]
    PACKETCATEGORIES[0][k] = obc.PACKETCATEGORIESOBC[k]
    PACKETCATEGORYSIZES[0][k] = obc.PACKETCATEGORYSIZESOBC[k]
    TABLECATEGORY[0][k] = obc.TABLECATEGORYOBC[k]
    TABLEDATA[0][k] = obc.TABLEDATAOBC[k]
    FILEDATACRUNCHING[0][k] = obc.FILEDATACRUNCHINGOBC[k]


# grab the PLD dictionnaries
for k in pld.CATEGORYREGISTRATIONPLD.keys():
    CATEGORYREGISTRATION[1][k] = pld.CATEGORYREGISTRATIONPLD[k]
    PACKETCATEGORIES[1][k] = pld.PACKETCATEGORIESPLD[k]
    PACKETCATEGORYSIZES[1][k] = pld.PACKETCATEGORYSIZESPLD[k]
    TABLECATEGORY[1][k] = pld.TABLECATEGORYPLD[k]
    TABLEDATA[1][k] = pld.TABLEDATAPLD[k]
    FILEDATACRUNCHING[1][k] = pld.FILEDATACRUNCHINGPLD[k]


ACKCATEGORIES = list(set(pld.ACKCATEGORIESPLD + obc.ACKCATEGORIESOBC))

RACKCAT = obc.RACKCAT
FACKCAT = obc.cmn.FACKCAT
EACKCAT = obc.cmn.EACKCAT
TELECOMMANDANSWERCAT = obc.cmn.TELECOMMANDANSWERCAT
