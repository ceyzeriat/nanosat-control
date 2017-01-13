#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .cm import Cm
from ..ccsds import TCPacker
from ..utils import core
#from .ccsds import ccsdsexception
from ..telecommand import Telecommand


__all__ = ['Command']


class Command(Cm):
    def __init__(self, *args, **kwargs):
        """
        Sends the command and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        # sole purpose of this __init__ is overwrite the docstring
        super(Command, self).__init__(*args, **kwargs)

    def _generate_packet(self, **kwargs):
        """
        Generates the full packet and returns the packet (str),
        the values used to generate the prim/sec headers (dict) and the
        input parameters used to generate the data (dict).
        """
        data, inputs = self.generate_data(**kwargs)
        packet, hd, hdx, dat = TCPacker.pack(pid=self.pid, data=data,
                                             tcid=self.number, retvalues=True,
                                             retdbvalues=True, **kwargs)
        return packet, hd, hdx, inputs

    def __call__(self, *args, **kwargs):
        return self.send(**kwargs)

    def send(self, *args, **kwargs):
        """
        Sends the command and stores it in the database

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
        hd['raw_file'] = core.RAWPACKETFILDER
        # saves to DB
        hd['time_sent'] = core.now()
        return Telecommand._initfromCommand(hd=hd, hdx=hdx, inputs=inputs)

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return self._generate_packet(**kwargs)

    @classmethod
    def _initfromCm(cls, cmd):
        return cls(**cmd.to_dict())
