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

from param import param_all
from .param_report import REPORTSDATA


__all__ = ['REPORTS', 'REPORTSDATA']


# init
REPORTS = {}


class Report(object):
    def __init__(self, key, message, params):
        """
        Base for reporting to watchdog

        Args:
        * key (str[15]): the str key-id of the report
        * message (str): the reporting message
        * params (iterable of str): the required parameters in the
          message
        """
        self.key = str(key)[:25]
        self.message = str(message)
        self.params = tuple(params)

    def pack(self, **kwargs):
        """
        Builds the socket-report to send

        Kwargs:
        * The parameters required for the report, see ``params`` attribute
        """
        dic = {}
        for k in self.params:
            dic[k] = kwargs.get(k, '')
        dic[param_all.REPORTKEY] = self.key
        return dic

    def disp(self, **kwargs):
        """
        Builds the reporting message

        Kwargs:
        * The parameters required for the reporting message, see
          ``params`` attribute
        """
        return self.message.format(**kwargs)


if not param_all.JUSTALIB:
    for key, message, params in REPORTSDATA:
        REPORTS[key] = Report(key=key, message=message, params=params)
