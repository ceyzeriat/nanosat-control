#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .cmd.command import Command
from .ccsds import CCSDSPacker
from .ccsds import param_ccsds
from .utils import core
#from .ccsds import ccsdsexception
from . import db


__all__ = ['Telecommand']


class Telecommand(Command):
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
        super(Telecommand, self).__init__(*args, **kwargs)
        self.pk = CCSDSPacker(mode='tc')

    def _generate_packet(self, **kwargs):
        """
        Generates the full packet and returns the packet (str),
        the values used to generate the prim/sec headers (dict) and the
        input parameters used to generate the data (dict).
        """
        data, inputs = self.generate_data(**kwargs)
        packet, hd, hdx, dat = self.pk.pack(pid=self.pid, data=data,
                                            tcid=self.number, retvalues=True,
                                            retdbvalues=True, **kwargs)
        return packet, hd, hdx, inputs

    def __call__(self, *args, **kwargs):
        return self.send(**kwargs)

    def send(self, *args, **kwargs):
        """
        Sends the telecommand and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        # generates the packet
        packet, hd, hdx, inputs = self._generate_packet(**kwargs)
        # save to server
        hd['raw_file'] = './raw_data'
        # saves to DB
        hd['time_sent'] = core.now()
        db.save_TC_to_DB(hd, hdx, inputs)
        # broadcast on socket to the antenna process
        # send(packet)

    def show(self, *args, **kwargs):
        return self._generate_packet(**kwargs)

    @classmethod
    def _initfromCommand(cls, cmd):
        return cls(**cmd.to_dict())
