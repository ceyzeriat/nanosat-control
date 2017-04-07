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
from ..ccsds import param_ccsds
from param import param_all
from param.param_apid import PIDREGISTRATION_REV

__all__ = ['XDISP']


locale.setlocale(locale.LC_ALL, '')
locale_code = locale.getpreferredencoding()


def e(txt):
    return txt.encode(locale_code)


LISTENICO = (9, u'\u260E')
CONTROLICO = (11, u'\u262D')
SAVEICO = (13, u'\u2744')

SENTICO = (75, u'\u2191')
RACKICO = (76, u'\u21AF')
FACKICO = (77, u'\u03A6')
EACKICO = (78, u'\u2020')

PAYLOADICO = u'\u03C0'
OBCICO = u'\u03A9'
L0ICO = u'\u2218'
L1ICO = u'\u25CE'
HORLINE = u'\u2500'

TCFMT = u'{timestamp} {pld} {lvl} {pid:<15} #{pkid:>5} {cmd_name:<27}'
TMFMT = u'{timestamp} {pld} {lvl} {pid:<15} #{pkid:>5} cat: {cat:>2} len: {sz:>3}'
MAXSTORETC = 100
MAXDISPLAYTC = 8
MAXSTORETM = 100
MAXDISPLAYTM = 8
MAXSTORERP = 100
MAXDISPLAYRP = 10

TIMEUPDFREQ = 3.
PRINTFREQ = 5.


"""
VERLINESPLITLEFT = u'\u2524'
VERLINESPLITRIGHT = u'\u251C'
UPLEFTCORNER = u'\u256D'
UPRIGHTCORNER = u'\u256E'
BOTTOMRIGHTCORNER = u'\u256F'
BOTTOMLEFTCORNER = u'\u2570'
VERLINE = u'\u2502'
HORLINESPLITUP = u'\u2534'
HORLINESPLITDOWN = u'\u252C'
CROSS = u'\u253C'
"""

class PrintOut(object):
    def __init__(self, text, loc, opts=None, newline=False):
        self.text = e(text)
        self.line = loc[0]
        self.col = loc[1]
        self.opts = opts
        self.newline = bool(newline)


class Xdisp(object):
    def __init__(self):
        self.running = False
        self.TClist = []
        self.TMlist = []
        self.printbuff = []

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
        self.TC.refresh()
        self.TM = newlinebox(MAXDISPLAYTM, self.width,
                                MAXDISPLAYTC+3, 0, "Telemetries")
        self.TM.refresh()
        self.RP = newlinebox(MAXDISPLAYRP, self.width,
                                MAXDISPLAYTM+MAXDISPLAYTC+4, 0, "Reporting")
        self.RP.refresh()
        time.sleep(0.1)  # give it a bit of air
        self.running = True
        self._disp(self.bar, PrintOut(' '*(self.width-1), (0, 0)))
        self.set_listenico(status=self.NOSTARTED)
        self.set_controlico(status=self.NOSTARTED)
        self.set_saveico(status=self.NOSTARTED)
        loopy = Thread(target=loop_time, args=(self,))
        loopy.daemon = True
        loopy.start()
        loopy = Thread(target=update_it, args=(self,))
        loopy.daemon = True
        loopy.start()
        self._key_catch()
        return

    def _disp(self, win, txt):
        self.printbuff.append((win, txt))

    def set_controlico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self._disp(self.bar,
                   PrintOut(CONTROLICO[1], (0, CONTROLICO[0]), opts=status))

    def set_saveico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self._disp(self.bar,
                   PrintOut(SAVEICO[1], (0, SAVEICO[0]), opts=status))

    def set_listenico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self._disp(self.bar,
                   PrintOut(LISTENICO[1], (0, LISTENICO[0]), opts=status))

    def set_time(self):
        """
        Sets the time
        """
        if not self.running:
            return
        self._disp(self.bar,
                   PrintOut(core.now().strftime('%T'), (0, 0), opts=self.BLUE))

    def report(self, message):
        """
        Adds the message to the reporting box
        """
        if not self.running:
            return
        self._disp(self.RP,
                   PrintOut('{} {}'.format(core.now().strftime('%T'), message),
                            (0, 0), opts=self.WHITE, newline=True))

    def set_TC_sent(self, packet_id, status):
        """
        Status can be OK, WAIT
        """
        if not self.running:
            return
        for idx, item in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self._disp(self.TC,
                           PrintOut(SENTICO[1], (idx, SENTICO[0]),
                                    opts=status))
                break

    def set_TC_rack(self, packet_id, status):
        """
        Status can be NONE, OK or WAIT
        """
        if not self.running:
            return
        for idx, item in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self._disp(self.TC,
                           PrintOut(RACKICO[1], (idx, RACKICO[0]),
                                    opts=status))
                break

    def set_TC_fack(self, packet_id, status):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for idx, item in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self._disp(self.TC,
                           PrintOut(FACKICO[1], (idx, FACKICO[0]),
                                    opts=status))
                break

    def set_TC_eack(self, packet_id, status):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for idx, item in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self._disp(self.TC,
                           PrintOut(EACKICO[1], (idx, EACKICO[0]),
                                    opts=status))
                break

    def add_TC(self, dbid, infos):
        dbid = int(dbid)
        if dbid in [item['dbid'] for item in self.TClist]:
            return
        if not self.running:
            return
        self.TClist = [infos] + self.TClist[:MAXSTORETC-1]
        cmdname = str(infos.get('cmdname'))
        pld = int(infos[param_ccsds.PAYLOADFLAG.name])
        lvl = int(infos[param_ccsds.LEVELFLAG.name])
        pid = int(infos[param_ccsds.PID.name])
        packet_id = str(infos[param_ccsds.PACKETID.name])
        self._disp(self.TC,
                   PrintOut(TCFMT.format(
                                timestamp=core.now().strftime("%F %T"),
                                pld=PAYLOADICO if pld == 1 else OBCICO,
                                lvl=L1ICO if lvl == 1 else L0ICO,
                                pid=PIDREGISTRATION_REV[pid][pld][lvl],
                                pkid=packet_id,
                                cmd_name=cmdname),
                            (0, 0), opts=self.WHITE, newline=True))
        self.set_TC_sent(packet_id, self.WAIT)
        self.set_TC_rack(packet_id,
                     self.WAIT if int(infos[\
                        param_ccsds.REQACKRECEPTIONTELECOMMAND.name]) == 1\
                            else self.NONE)
        self.set_TC_fack(packet_id,
                     self.WAIT if int(infos[\
                        param_ccsds.REQACKFORMATTELECOMMAND.name]) == 1\
                            else self.NONE)
        self.set_TC_eack(packet_id,
                     self.WAIT if int(infos[\
                        param_ccsds.REQACKEXECUTIONTELECOMMAND.name]) == 1\
                            else self.NONE)

    def add_TM(self, pkid, infos):
        pkid = int(pkid)
        if pkid in [item[param_ccsds.PACKETID.name] for item in self.TMlist]:
            return
        if not self.running:
            return
        self.TMlist = [infos] + self.TMlist[:MAXSTORETM-1]
        pld = int(infos[param_ccsds.PAYLOADFLAG.name])
        lvl = int(infos[param_ccsds.LEVELFLAG.name])
        pid = int(infos[param_ccsds.PID.name])
        cat = int(infos[param_ccsds.PACKETCATEGORY.name])
        self._disp(self.TM,
                   PrintOut(TMFMT.format(
                                timestamp=core.now().strftime("%F %T"),
                                pld=PAYLOADICO if pld == 1 else OBCICO,
                                lvl=L1ICO if lvl == 1 else L0ICO,
                                pid=PIDREGISTRATION_REV[pid][pld][lvl],
                                pkid=pkid,
                                cat=cat,
                                sz=infos['sz']),
                            (0, 0), opts=self.WHITE, newline=True))

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
        self.NOSTARTED = self.BLUE
        self.ALIVE = self.GREEN
        self.DEAD = self.RED
        self.NONE = self.BLUE
        self.OK = self.GREEN
        self.ERROR = self.RED
        self.WAIT = self.YELLOW
        
    def _key_catch(self):
        while self.running:
            self.RP.move(0, 0)
            #self.RP.addstr(0, 0, ">")
            self.RP.clrtoeol()
            s = self.RP.getstr()
            if s == "q":
                self.running = False
            #self.RP.insertln()
            #self.RP.addstr(1, 0, "[" + s + "]")


def update_it(self):
    while self.running:
        # make local copy of list
        for win, item in list(self.printbuff):
            if item.newline:
                win.move(item.line, 0)
                win.insertln()
            if item.opts is None:
                win.addstr(item.line, item.col, item.text)
            else:
                win.addstr(item.line, item.col, item.text, item.opts)
            win.refresh()
            self.printbuff.pop(0)
        time.sleep(1./PRINTFREQ)


def newlinebox(h, w, y, x, title=None):
    wb = curses.newwin(2, w, y-1, x)
    wb.addstr(0, 0, e(HORLINE)*(w-x))
    if title is not None:
        wb.addstr(0, 2, e(title))
    wb.refresh()
    return curses.newwin(h, w, y, x)


def loop_time(self):
    while self.running:
        self.set_time()
        time.sleep(1./TIMEUPDFREQ)


if not param_all.JUSTALIB:
    XDISP = Xdisp()
