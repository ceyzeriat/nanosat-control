#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..utils.core import datetime


__all__ = ['Ms']


class Ms(int):
    def __init__(self, v):
        super(int, self).__init__(v)
        self._hour = self // 3600000
        self._min = (self % 3600000) // 60000
        self._sec = (self % 60000) // 1000
        self._msec = self % 1000
        self._time = datetime.time(self._hour, self._min, self._sec,
                                   self._sec*1000)

    def strf(self, fmt='%H:%M:%S'):
        """
        Returns the formatted string of the time

        Args:
        * fmt (time format): %H=hours, %M=minutes, %S=seconds,
          %f=microseconds. Check:
          https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        """
        return self._time.strftime(fmt)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        pass

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        pass

    @property
    def sec(self):
        return self._sec

    @sec.setter
    def sec(self, value):
        pass

    @property
    def msec(self):
        return self._msec

    @msec.setter
    def msec(self, value):
        pass
