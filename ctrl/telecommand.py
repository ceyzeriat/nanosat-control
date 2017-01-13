#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .utils import core
#from .ccsds import ccsdsexception
from . import db


__all__ = ['Telecommand']


class Telecommand(object):
    def __init__(self, *args, **kwargs):
        """
        Sends the telecommand and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        pass

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return self._generate_packet(**kwargs)

    @classmethod
    def _initfromCommand(cls, hd, hdx, inputs):
        tcid = db.save_TC_to_DB(hd, hdx, inputs)
        # broadcast on socket to the antenna process
        # send(packet)
        return cls(**cmd.to_dict())
