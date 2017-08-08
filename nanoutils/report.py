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

from . import param_sys
from .param_report import REPORTSDATA, EXTRADISPKEY


__all__ = ['REPORTS', 'REPORTSDATA', 'EXTRADISPKEY']


class Report(object):
    def __init__(self, key, message, params, prt=True):
        """
        Base for reporting to watchdog

        Args:
          * key (str[25]): the str key-id of the report
          * message (str): the reporting message with param fmt {tags}
          * params (iterable of str): the required parameters in the
            message
          * prt (bool): [opt] to print or not this reporting
        """
        self.key = str(key)[:25]
        self.message = str(message)
        self.params = tuple(params)
        self.prt = bool(prt)

    def pack(self, **kwargs):
        """
        Builds the socket-report to send

        Kwargs:
        * The parameters required for the report, see ``params`` attribute
        """
        dic = {}
        for k in self.params:
            dic[k] = kwargs.get(k, '')
        # add the print key
        dic[EXTRADISPKEY] = kwargs.get(EXTRADISPKEY, self.prt)
        dic[param_sys.REPORTKEY] = self.key
        return dic

    def disp(self, **kwargs):
        """
        Builds the reporting message

        Kwargs:
          * The parameters required for the reporting message, see
            ``params`` attribute
        """
        if self.prt:
            return self.message.format(**kwargs)
        else:
            return ''


# init
REPORTS = {}
for pp in REPORTSDATA:
    key, message, params = pp[:3]
    if len(pp) == 3:
        REPORTS[key] = Report(key=key, message=message, params=params)
    elif len(pp) == 4:
        REPORTS[key] = Report(key=key, message=message,
                              params=params, prt=bool(pp[3]))

