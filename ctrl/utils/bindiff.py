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


from byt import Byt
from .slc import Slc


__all__ = ['Bindiff']


class Bindiff(object):
    def __init__(self, old, new, overhead, maxbuff, emptychar=None):
        """
        Does the binary difference

        Args:
        * old (bytes): the reference (old) binary data
        * new (bytes): the new binary data to be compared
        * overhead (int): the size of headers associated to the bin-data
        * maxbuff (int): the maximum size of bin-data
        * emptychar (byte): the padding character if the new bin-data is
            shorter than the reference, or `None` for no padding
        """
        self.overhead = int(overhead)
        self.maxbuff = int(maxbuff)
        self.padding = (emptychar is None)        
        self.emptychar = Byt(emptychar)[0]
        self.new = Byt(new)
        self.old = Byt(old)
        cutit = len(self.new)
        self.newlen = len(self.new)
        self.oldlen = len(self.old)        
        # if new bin-data is shorter than old
        if cutit < len(self.old):
            # if padding is requested, pad the new bin with eptychar
            if self.padding:
                self.new += self.emptychar * (self.oldlen - self.newlen)
                self.newlen = self.oldlen
            # else, shorten the old bin-data
            else:
                self.old = self.old[:cutit]
                self.oldlen = self.newlen                
        self.minlen = min(self.oldlen, self.newlen)
        self.maxlen = max(self.oldlen, self.newlen)
            

    def do_it(self):
        """
        Performs the binary comparison, optimization and slicing
        """
        slices = self.slice_it()
        slcs = self.optimize_slices(slices)
        return self.generate_slices(slices if slcs is False else slcs)

    def slice_it(self):
        """
        Generates the list of slices that represent differences
        """
        buffing = False
        slices = []
        for idx, (bav, bap) in enumerate(zip(   str(self.old[:self.minlen]),
                                                str(self.new[:self.minlen]))):
            if bav != bap and not buffing:
                slices.append(Slc(s=idx))
                buffing = True
            elif bav != bap and buffing:
                if slices[-1].l < self.maxbuff:
                    slices[-1].inc()
                else:
                    slices.append(Slc(s=idx))
            elif bav == bap and buffing:
                buffing = False
        if self.oldlen != self.newlen:
            pos = self.minlen
            for idx in xrange((self.maxlen-pos) // self.maxbuff + 1):
                slices.append(Slc(  s=pos,
                                    l=min(self.maxbuff, self.maxlen-pos)))
                pos += self.maxbuff
        return slices

    def optimize_slices(self, slices):
        """
        Optimizes the list of slices
        """
        ltot = sum([s.l + self.overhead for s in slices])
        if len(slices) < 2:
            return slices
        at_least_one = False
        newltot = ltot
        for idx, (sl, slp) in enumerate(zip(list(slices[:-1]),
                                            list(slices[1:]))):
            nsz = (sl + slp).l
            diff = sl.l + slp.l + self.overhead - nsz
            if diff > 0 and nsz < self.maxbuff and newltot >= ltot - diff:
                at_least_one = True
                newblocks = slices[:idx] + [sl+slp] + slices[idx+2:]
                res = self.optimize_slices(newblocks)
                if res is False:
                    continue
                else:
                    return res
        else:
            if not at_least_one:
                return False
            else:
                return newblocks

    def generate_slices(self, slices):
        """
        Returns the list of data blocks
        """
        blocks = {}
        for sl in slices:
            blocks[sl.s] = Byt(self.new[sl.slice()])
        return blocks
