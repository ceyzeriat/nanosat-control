#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .core import *
exc = core.ccsdsexception


__all__ = ['CCSDSKey']


class CCSDSKey(object):
    def __init__(self, name, dic, start, end=None, fct=None, unit=''):
        """
        Dictionary of keys to perform easy extraction from a bits sequence
        
        Args:
        * name (str): the name of the dictionary, for debug purposes
        * dic (dict): dictionary of possible values
        * start (int): start-position in bit from the beginning of the primary
          header, or whatever reference you decided
        * end (int) [optional]: end-position (inclusive) in bit from the
          beginning of primary header, or whatever reference you decided.
          Default is equal to ``start`` (length = 1)
        * fct (callable) [optional]: function to apply on the output bits
        * unit (str) [optional]: the unit of the output value
        """
        self.name = str(name)
        self.dic = dict(dic)
        self.cut = slice(int(start),
                         int(end)+1 if end is not None else int(start)+1)
        self.fct = fct if callable(fct) else None

    def __str__(self):
        return "{}: {} <{}>{}".format(self.name,
                                      self.dic,
                                      self.cut,
                                      ", fct: {}".format(self.fct.func_name)\
                                          if self.fct is not None else "")

    __repr__ = __str__

    def __getitem__(self, key):
        if key in self.dic.keys():
            return self.dic[key]
        elif str(key) in self.dic.keys():
            return self.dic[str(key)]
        else:
            try:
                return self.dic[int(key)]
            except:
                raise exc.NoSuchKey(dic=self.dic, key=key)

    def grab(self, bits, raw=False, *kwargs):
        """
        Grabs the slice of relevant bits and returns the corresponding
        dictionary key or applies the transform function if applicable

        Args:
        * bits (str): chain of '0' and '1'
        * raw (bool): if ``True``, returns the raw bit sequence
        """
        dum = bits[self.cut]
        if raw:
            return dum
        elif self.fct is None:
            return self.find(dum)
        else:
            return self.fct(dum, *kwargs)

    def find(self, value):
        """
        Performs the reverse search in the dictionary: given a
        value, it will return the corresponding key

        Args:
        * value: the value to search in ``dic``
        """
        for k, v in self.dic.items():
            if v == value:
                return k
            elif str(v) == str(value):
                return k
            else:
                try:
                    if int(v) == int(value):
                        return k
                except:
                    pass
        else:
            raise exc.NoSuchKey(dic=self.dic, key=key)
