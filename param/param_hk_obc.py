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
from ctrl.ccsds.ccsdsmetatrousseau import CCSDSMetaTrousseau

#from . import param_category_obc
from .generated.l0hkstructpart1 import L0HKSTRUCTPART1_KEYS
from .generated.l0hkstructpart2 import L0HKSTRUCTPART2_KEYS


__all__ = ['TROUSSEAU']


class CCSDSTrousseauHKOBC(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        # appel méthode mère
        res = super(CCSDSTrousseauHKOBC, self).unpack(data, **kwargs)
        # pour chaque clé
        for item in self.keys:
            # est-ce qu'il y a un convertion
            if item.unram is not None:
                # on ajoute dans le dictionnaire de résultat
                res[item.name+'_phys'] = item.unram(res[item.name], **kwargs)
        return res

    def _make_fmt(self, splt=''):
        self.fmt = splt.join(["%s:{%s} ({%s})" %\
                                (key.disp, key.name, key.name+'_phys')\
                                    for key in self.keys])


TROUSSEAUDICT = {0: CCSDSTrousseauHKOBC(L0HKSTRUCTPART1_KEYS),
                 1: CCSDSTrousseauHKOBC(L0HKSTRUCTPART2_KEYS)}


TROUSSEAU = CCSDSMetaTrousseau(TROUSSEAUDICT, key='hk_part')
