#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .core import DATETIME_REF, datetime, time


__all__ = ['Day']


class Day(int):
    def __init__(self, v):
        super(int, self).__init__(v)
        d = time.gmtime((DATETIME_REF + self) * 86400)        
        self._year = d.tm_year
        self._month = d.tm_mon
        self._day = d.tm_mday
        self._date = datetime.date(self._year, self._month, self._day)

    def strf(self, fmt='%Y/%m/%d'):
        """
        Returns the formatted string of the time

        Args:
        * fmt (time format): check
          https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        """
        return self._date.strftime(fmt)

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        pass

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        pass

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        pass
