#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .utils import core
#from .ccsds import ccsdsexception
from . import db


__all__ = ['Order']


class Order(object):
    def __init__(self, hd, hdx, inputs):
        """
        hop
        """
        self.hd = dict(hd)
        self.hdx = dict(hdx)
        self.inputs = dict(inputs)
