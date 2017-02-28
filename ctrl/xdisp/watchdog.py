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

__all__ = ['Xdisp']


locale.setlocale(locale.LC_ALL, '')


LISTENICO = (9, u'\u260E '.encode('utf-8'))
CONTROLICO = (11, u'\u262D '.encode('utf-8'))
SAVEICO = (13, u'\u26C3 '.encode('utf-8'))
PAYLOADICO = u'\u03C0'.encode('utf-8')
OBCICO = u'\u03A9'.encode('utf-8')
L0ICO = u'\u24DE'.encode('utf-8')
L1ICO = u'\u2461'.encode('utf-8')

"""
UPLEFTCORNER = u'\u256D'.encode('utf-8')
UPRIGHTCORNER = u'\u256E'.encode('utf-8')
BOTTOMRIGHTCORNER = u'\u256F'.encode('utf-8')
BOTTOMLEFTCORNER = u'\u2570'.encode('utf-8')
HORLINE = u'\u2500'.encode('utf-8')
VERLINE = u'\u2502'.encode('utf-8')
HORLINESPLITUP = u'\u2534'.encode('utf-8')
HORLINESPLITDOWN = u'\u252C'.encode('utf-8')
VERLINESPLITLEFT = u'\u2524'.encode('utf-8')
VERLINESPLITRIGHT = u'\u251C'.encode('utf-8')
CROSS = u'\u253C'.encode('utf-8')
"""


def newlinebox(h, w, y, x, title=None):
    wb = curses.newwin(2, w, y-1, x)
    wb.addstr(0, 0, u"-"*80)
    if title is not None:
        wb.addstr(0, 2, title.encode('utf-8'))
    wb.refresh()
    return curses.newwin(h, w, y, x)

def loop_time(self, freq):
    while self.running:
        self.set_time()
        time.sleep(1./freq)

class Xdisp(object):
    def __init__(self):
        pass

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
        self.TC = newlinebox(8, self.width, 2, 0, "Telecommands")
        self.TM = newlinebox(8, self.width, 11, 0, "Telemetries")
        self.RP = newlinebox(8, self.width, 20, 0, "Reporting")
        self.set_controlico(status=self.NOSTARTED)
        self.set_saveico(status=self.NOSTARTED)
        self.set_listenico(status=self.NOSTARTED)
        self.TC.refresh()
        self.TM.refresh()
        self.running = True
        self._start_set_time(3)
        self._loopit()

    def set_controlico(self, status):
        self.bar.addstr(0, CONTROLICO[0], CONTROLICO[1], status)

    def set_saveico(self, status):
        self.bar.addstr(0, SAVEICO[0], SAVEICO[1], status)

    def set_listenico(self, status):
        self.bar.addstr(0, LISTENICO[0], LISTENICO[1], status)

    def _start_set_time(self, freq=3):
        loopy = Thread(target=loop_time, args=(self, float(freq)))
        loopy.daemon = True
        loopy.start()

    def set_time(self):
        self.bar.addstr(0, 0, core.now().strftime('%H:%M:%S'), self.BLUE)
        self.bar.refresh()

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
        
    def _loopit(self):
        while self.running:
            self.RP.addstr(0, 0, ">")
            self.RP.clrtoeol()
            s = self.RP.getstr()
            if s == "q":
                self.running = False
            self.RP.insertln()
            self.RP.addstr(1, 0, "[" + s + "]")
        self.running = False
