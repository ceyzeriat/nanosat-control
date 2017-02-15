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

locale.setlocale(locale.LC_ALL, '')


CONTROLICO = u'\u262D '.encode('utf-8')
SAVEICO = u'\u26C3 '.encode('utf-8')
LISTENICO = u'\u260E '.encode('utf-8')

UPLEFTCORNER = u'\u256D'
UPRIGHTCORNER = u'\u256E'
BOTTOMRIGHTCORNER = u'\u256F'
BOTTOMLEFTCORNER = u'\u2570'
HORLINE = u'\u2500'
VERLINE = u'\u2502'
HORLINESPLITUP = u'\u2534'
HORLINESPLITDOWN = u'\u252C'
VERLINESPLITLEFT = u'\u2524'
VERLINESPLITRIGHT = u'\u251C'
CROSS = u'\u253C'



def newwinbox(h, w, y, x, inbox=False):
    if not inbox:
        h += 2
        w += 2
        y -= 1
        x -= 1
    wb = curses.newwin(h, w, y, x)
    wb.box()
    wb.refresh()
    return curses.newwin(h-2, w-2, y+1, x+1)

class Xdisp(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.start_color()
        curses.use_default_colors()
        curses.echo()
        self._init_colors()
        self.stdscr.border()
        self.stdscr.refresh()
        self.report = newwinbox(5, 40, 6, 20)
        self.process = newwinbox(3, 33, 13, 19)
        self.set_controlico()
        self.set_saveico()
        self.set_listenico()
        self.process.refresh()
        self.loopit()

    def set_controlico(self, status=0):
        self.process.addstr(0,0, CONTROLICO, self.BLACK)

    def set_saveico(self, status=0):
        self.process.addstr(0,2, SAVEICO, self.RED)

    def set_listenico(self, status=0):
        self.process.addstr(0,4, LISTENICO, self.GREEN)

    def _init_colors(self):
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.BLACK = curses.color_pair(1)
        self.RED = curses.color_pair(2)
        self.GREEN = curses.color_pair(3)
        
    def loopit(self):
        while True:
            self.report.addstr(0, 0, ">")
            self.report.clrtoeol()
            s   = self.report.getstr()
            if s == "q":
                break
            self.report.insertln()
            self.report.addstr(1, 0, "[" + s + "]")

curses_main = curses.wrapper(Xdisp)
