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


import curses
import locale
import time
from threading import Thread
from ..utils import core
from param import param_all

__all__ = ['XDISP']


locale.setlocale(locale.LC_ALL, '')


def e(txt):
    return txt.encode('utf-8')


LISTENICO = (9, e(u'\u260E '))
CONTROLICO = (11, e(u'\u262D '))
SAVEICO = (13, e(u'\u26C3 '))

SENTICO = (50, e(u'\u2191'))
RACKICO = (53, e(u'\u21AF'))
FACKICO = (56, e(u'\U0001D122'))
EACKICO = (59, e(u'\u2020'))

PAYLOADICO = e(u'\u03C0')
OBCICO = e(u'\u03A9')
L0ICO = e(u'\u24DE')
L1ICO = e(u'\u2461')
HORLINE = e(u'\u2500')

TCFMT = e('{timestamp} {pld}  {lvl}  {pid:15<} {pkid:5>} {cmd_name:18>}')
MAXSTORETC = 100
MAXDISPLAYTC = 8
MAXSTORETM = 100
MAXDISPLAYTM = 8
MAXSTORERP = 100
MAXDISPLAYRP = 8


"""
VERLINESPLITLEFT = e(u'\u2524')
VERLINESPLITRIGHT = e(u'\u251C')
UPLEFTCORNER = e(u'\u256D')
UPRIGHTCORNER = e(u'\u256E')
BOTTOMRIGHTCORNER = e(u'\u256F')
BOTTOMLEFTCORNER = e(u'\u2570')
VERLINE = e(u'\u2502')
HORLINESPLITUP = e(u'\u2534')
HORLINESPLITDOWN = e(u'\u252C')
CROSS = e(u'\u253C')
"""


def newlinebox(h, w, y, x, title=None):
    wb = curses.newwin(2, w, y-1, x)
    wb.addstr(0, 0, HORLINE*80)
    if title is not None:
        wb.addstr(0, 2, title)
    wb.refresh()
    return curses.newwin(h, w, y, x)

def loop_time(self, freq):
    while self.running:
        self.set_time()
        time.sleep(1./freq)

class Xdisp(object):
    def __init__(self):
        self.running = False
        self.TClist = []
        self.TMlist = []

    def start(self):
        curses.wrapper(self.init)

    def init(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.height, self.width = stdscr.getmaxyx()
        curses.start_color()
        curses.use_default_colors()
        curses.echo()
        self._init_colors()
        self.bar = curses.newwin(1, self.width, 0, 0)
        self.TC = newlinebox(MAXDISPLAYTC, self.width,
                                2, 0, "Telecommands")
        self.TM = newlinebox(MAXDISPLAYTM, self.width,
                                MAXDISPLAYTC+3, 0, "Telemetries")
        self.RP = newlinebox(MAXDISPLAYRP, self.width,
                                MAXDISPLAYTM+MAXDISPLAYTC+4, 0, "Reporting")
        self.running = True
        self.set_controlico(status=self.NOSTARTED)
        self.set_saveico(status=self.NOSTARTED)
        self.set_listenico(status=self.NOSTARTED)
        self.TC.refresh()
        self.TM.refresh()
        self._start_set_time(3)
        self._loopit()
        return

    def set_controlico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.bar.addstr(0, CONTROLICO[0], CONTROLICO[1], status)

    def set_saveico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.bar.addstr(0, SAVEICO[0], SAVEICO[1], status)

    def set_listenico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.bar.addstr(0, LISTENICO[0], LISTENICO[1], status)

    def _start_set_time(self, freq=3):
        loopy = Thread(target=loop_time, args=(self, float(freq)))
        loopy.daemon = True
        loopy.start()

    def set_time(self):
        """
        Sets the time
        """
        if not self.running:
            return
        self.bar.addstr(0, 0, core.now().strftime('%T'), self.BLUE)
        self.bar.refresh()

    def report(self, message):
        """
        Adds the message to the reporting box
        """
        if not self.running:
            return
        self.RP.move(0, 0)
        self.RP.insertln()
        self.RP.addstr(0, 0, '{} {}'.format(core.now().strftime('%T'),\
                                            message), self.WHITE)
        self.RP.refresh()

    def set_TC_sent(self, dbid, statut):
        """
        Status can be OK, WAIT
        """
        if not self.running:
            return
        for item in self.TClist[:MAXDISPLAYTC]:
            if dbid == item['dbid']:
                self.TC.addstr(line, SENTICO[0], SENTICO[1], status)
        self.TC.refresh()

    def set_TC_rack(self, dbid, statut):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for item in self.TClist[:MAXDISPLAYTC]:
            if dbid == item['dbid']:
                self.TC.addstr(line, RECICO[0], RECICO[1], status)
        self.TC.refresh()

    def set_TC_fack(self, dbid, statut):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for item in self.TClist[:MAXDISPLAYTC]:
            if dbid == item['dbid']:
                self.TC.addstr(line, FORMATICO[0], FORMATICO[1], status)
        self.TC.refresh()

    def set_TC_eack(self, dbid, statut):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for item in self.TClist[:MAXDISPLAYTC]:
            if dbid == item['dbid']:
                self.TC.addstr(line, EXEICO[0], EXEICO[1], status)
        self.TC.refresh()

    def add_TC(self, dbid, cmdname, hd, hdx, inputs):
        if dbid in [item['dbid'] for item in self.TClist]:
            return
        if not self.running:
            return
        hd['dbid'] = dbid
        hd.update(hdx)
        hd.update(inputs)
        self.TClist = [hd] + self.TClist[:MAXSTORETC-1]
        self.TC.move(0, 0)
        self.TC.insertln()
        self.TC.addstr(0, 0, TCFMT.format(
                            timestamp=e(core.now().strftime("%F %T")),
                            pld=PAYLOADICO if int(hd['payload_flag']) == 1\
                                else OBCICO,
                            lvl=L1ICO if int(hd['level_flag']) == 1\
                                else L0ICO,
                            pid=e(hd['pid']),
                            pkid=e(str(hd['packet_id'])),
                            cmd_name=e(cmdname)),
                        self.WHITE)
        self.set_TC_sent(dbid, self.WAIT)
        self.set_TC_rack(dbid, self.WAIT if int(hd['reqack_reception']) == 1\
                                            else self.NONE)
        self.set_TC_fack(dbid, self.WAIT if int(hd['reqack_format']) == 1\
                                            else self.NONE)
        self.set_TC_eack(dbid, self.WAIT if int(hd['reqack_execution']) == 1\
                                            else self.NONE)

    def _init_colors(self):
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.WHITE = curses.color_pair(0)
        self.BLACK = curses.color_pair(1)
        self.RED = curses.color_pair(2)
        self.GREEN = curses.color_pair(3)
        self.YELLOW = curses.color_pair(4)
        self.BLUE = curses.color_pair(5)
        self.PURPLE = curses.color_pair(6)
        self.CYAN = curses.color_pair(7)
        self.NOSTARTED = self.BLACK
        self.ALIVE = self.GREEN
        self.DEAD = self.RED
        self.NONE = self.BLACK
        self.OK = self.GREEN
        self.ERROR = self.RED
        self.WAIT = self.BLUE
        
    def _loopit(self):
        while self.running:
            self.RP.move(0, 0)
            #self.RP.addstr(0, 0, ">")
            self.RP.clrtoeol()
            s = self.RP.getstr()
            if s == "q":
                self.running = False
            #self.RP.insertln()
            #self.RP.addstr(1, 0, "[" + s + "]")

if not param_all.JUSTALIB:
    XDISP = Xdisp()

#XDISP.start()
