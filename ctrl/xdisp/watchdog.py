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

import os
os.environ.setdefault('ESCDELAY', '25')
import curses
import curses.panel
import locale
import time
from threading import Thread
from byt import Byt
from ..utils import core
from ..ccsds import param_ccsds
from param import param_all
from param.param_apid import PIDREGISTRATION_REV
from param import param_category


__all__ = ['XDISP']

locale.setlocale(locale.LC_ALL, '')
locale_code = locale.getpreferredencoding()


MAXSTORETC = 100
MAXDISPLAYTC = 8
MAXSTORETM = 100
MAXDISPLAYTM = 8
MAXSTORERP = 100
MAXDISPLAYRP = 10

TIMEUPDFREQ = 3.
PRINTFREQ = 10.
TIMESTAMPFMT = '%Y-%m-%d %H:%M:%S'


TCFMT = '{timestamp} {pld} {lvl} {pid:<15.15} #{pkid:<5.5} {cmd_name:<27.27}'
TMFMT = '{timestamp} {pld} {lvl} {pid:<15.15} #{pkid:<5.5} cat: {cat:>13.13} '\
        '({catnum:>2.2}) len: {sz:>3.3}'

HELP =\
"""
Shortcuts:
  * ESC: close pop-up
  * h: help
  * TAB: change panel TC>TM>Report>
  * UP:
  * DOWN: 
"""

# do we want to use unicode ?
if param_all.SHOWUNICODE:
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

    TCFMT = u'{timestamp} {pld} {lvl} {pid:<15.15} #{pkid:<5.5} {cmd_name:<27.27}'
    TMFMT = u'{timestamp} {pld} {lvl} {pid:<15.15} #{pkid:<5.5} cat: {cat:>13.13} '\
             '({catnum:>2.2}) len: {sz:>3.3}'
else:
    def e(txt):
        return txt


    LISTENICO = (9, 'L')
    CONTROLICO = (11, 'C')
    SAVEICO = (13, 'S')

    SENTICO = (75, 's')
    RACKICO = (76, 'r')
    FACKICO = (77, 'f')
    EACKICO = (78, 'e')

    PAYLOADICO = 'p'
    OBCICO = 'o'
    L0ICO = '0'
    L1ICO = '1'
    HORLINE = '-'


class PrintOut(object):
    def __init__(self, text, loc=(0,0), opts=None, newline=False):
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
        self.BOXSIZE = {0: MAXDISPLAYTC, 1: MAXDISPLAYTM, 2: MAXDISPLAYRP}

    def start(self):
        curses.wrapper(self.init)

    def init(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.height, self.width = stdscr.getmaxyx()
        curses.start_color()
        curses.use_default_colors()
        #curses.echo()
        self._init_colors()
        self.bar = curses.newwin(1, self.width, 0, 0)
        self.bar.keypad(True)
        self.barpan = curses.panel.new_panel(self.bar)
        self.TC, self.TCpan, self._TC, self._TCpan =\
                            newlinebox(MAXDISPLAYTC, self.width,
                                       2, 0, "Telecommands")
        self.TC.scrollok(True)
        self.TC.idlok(True)
        self.TC.refresh()
        self.TM, self.TMpan, self._TM, self._TMpan =\
                            newlinebox(MAXDISPLAYTM, self.width,
                                       MAXDISPLAYTC+3, 0, "Telemetries")
        self.TM.scrollok(True)
        self.TM.idlok(True)
        self.TM.refresh()
        self.RP, self.RPpan, self._RP, self._RPpan =\
                            newlinebox(MAXDISPLAYRP, self.width,
                                       MAXDISPLAYTM+MAXDISPLAYTC+4, 0, "Reporting")
        self.RP.refresh()
        self.updpan()
        time.sleep(0.2)  # give it a bit of air
        self.pan_box = 0
        self.PANBOX = {0: self.TC, 1: self.TM}
        self.pan_loc = {0: 0, 1: 0, 2: 0}
        self.running = True
        #self.bar.erase()refresh
        self.disp(self.bar, PrintOut(' '*(self.width-1)))
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

    def updpan(self):
        curses.panel.update_panels()
        self.stdscr.refresh()

    def disp(self, win, txt):
        self.printbuff.append((win, txt))

    def set_controlico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.disp(self.bar,
                   PrintOut(CONTROLICO[1], loc=(0, CONTROLICO[0]), opts=status))

    def set_saveico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.disp(self.bar,
                   PrintOut(SAVEICO[1], loc=(0, SAVEICO[0]), opts=status))

    def set_listenico(self, status):
        """
        Status can be NOSTARTED, ALIVE or DEAD
        """
        if not self.running:
            return
        self.disp(self.bar,
                   PrintOut(LISTENICO[1], loc=(0, LISTENICO[0]), opts=status))

    def set_time(self):
        """
        Sets the time
        """
        if not self.running:
            return
        self.disp(self.bar,
                   PrintOut(core.now().strftime('%T'), opts=self.CYAN))
        """ts = core.now().totimestamp()
        if int(ts%3) == 0 and getattr(self, 'last_ts', 0) != ts//3:
            self.last_ts = ts//3
            DEL = PrintOut("{}: here is a new line mate".format(len(self.TClist)),
                           opts=self.RED, newline=True)
            self.TClist = [(DEL, {})] + self.TClist[:MAXSTORETC-1]
            self.disp(0, DEL)
        """

    def report(self, message):
        """
        Adds the message to the reporting box
        """
        if not self.running:
            return
        self.disp(self.RP,
                  PrintOut('{} {}'.format(core.now().strftime('%T'), message),
                           opts=self.WHITE, newline=True))

    def set_TC_sent(self, packet_id, status):
        """
        Status can be OK, WAIT
        """
        if not self.running:
            return
        for idx, (txt, item) in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self.disp(0, PrintOut(SENTICO[1], loc=(idx, SENTICO[0]),
                                   opts=status))
                break

    def set_TC_rack(self, packet_id, status):
        """
        Status can be NONE, OK or WAIT
        """
        if not self.running:
            return
        if str(packet_id).lower() == 'none':
            # if no packet_id given.. just assume it is the RACK of the
            # lastest TC, index 0
            self.disp(0, PrintOut(RACKICO[1], loc=(0, RACKICO[0]),
                                    opts=status))
            return
        packet_id = int(packet_id)
        for idx, (txt, item) in enumerate(self.TClist[:MAXDISPLAYTC]):
            if packet_id == int(item[param_ccsds.PACKETID.name]):
                self.disp(0, PrintOut(RACKICO[1], loc=(idx, RACKICO[0]),
                                        opts=status))
                break

    def set_TC_fack(self, packet_id, status):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for idx, (txt, item) in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self.disp(0, PrintOut(FACKICO[1], loc=(idx, FACKICO[0]),
                                        opts=status))
                break

    def set_TC_eack(self, packet_id, status):
        """
        Status can be NONE, OK, WAIT or FAIL
        """
        if not self.running:
            return
        for idx, (txt, item) in enumerate(self.TClist[:MAXDISPLAYTC]):
            if int(packet_id) == int(item[param_ccsds.PACKETID.name]):
                self.disp(0, PrintOut(EACKICO[1], loc=(idx, EACKICO[0]),
                                       opts=status))
                break

    def add_TC(self, packet_id, infos):
        packet_id = int(packet_id)
        if packet_id in [item[param_ccsds.PACKETID.name]\
                                for (txt, item) in self.TClist]:
            return
        if not self.running:
            return
        pld = int(infos[param_ccsds.PAYLOADFLAG.name])
        lvl = int(infos[param_ccsds.LEVELFLAG.name])
        pid = int(infos[param_ccsds.PID.name])
        pidstr = str(PIDREGISTRATION_REV[pid][pld][lvl])\
                        if pid in PIDREGISTRATION_REV.keys() else "?????"
        TC = PrintOut(TCFMT.format(timestamp=core.now().strftime(TIMESTAMPFMT),
                                   pld=PAYLOADICO if pld == 1 else OBCICO,
                                   lvl=L1ICO if lvl == 1 else L0ICO,
                                   pid=pidstr,
                                   pkid=str(packet_id),
                                   cmd_name=str(infos.get('cmdname'))),
                      opts=self.WHITE, newline=True)
        self.TClist = [(TC, infos)] + self.TClist[:MAXSTORETC-1]
        self.disp(0, TC)
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

    def add_TM(self, packet_id, infos):
        packet_id = int(packet_id)
        if packet_id in [item[param_ccsds.PACKETID.name]\
                                    for (txt, item) in self.TMlist]:
            return
        if not self.running:
            return
        pld = int(infos[param_ccsds.PAYLOADFLAG.name])
        lvl = int(infos[param_ccsds.LEVELFLAG.name])
        pid = int(infos[param_ccsds.PID.name])
        catnum = int(infos[param_ccsds.PACKETCATEGORY.name])
        cat = param_category.CATEGORIES[pld][catnum]
        TM = PrintOut(TMFMT.format(timestamp=core.now().strftime(TIMESTAMPFMT),
                                   pld=PAYLOADICO if pld == 1 else OBCICO,
                                   lvl=L1ICO if lvl == 1 else L0ICO,
                                   pid=str(PIDREGISTRATION_REV[pid][pld][lvl]),
                                   pkid=str(packet_id),
                                   cat=str(cat.name),
                                   catnum=str(catnum),
                                   sz=str(infos['_sz_blobish'])),
                      opts=self.WHITE, newline=True)
        self.TMlist = [(TM, infos)] + self.TMlist[:MAXSTORETM-1]
        self.disp(1, TM)

    def _init_colors(self):
        for i in range(curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        for i in range(curses.COLORS):
            curses.init_pair(i + curses.COLORS, i, 0)
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
        curses.init_pair(8, 7, 0)
        self.WHITE_BG = curses.color_pair(8)
        self.RED_BG = curses.color_pair(9)
        self.GREEN_BG = curses.color_pair(10)
        self.YELLOW_BG = curses.color_pair(11)
        self.BLUE_BG = curses.color_pair(12)
        self.PURPLE_BG = curses.color_pair(13)
        self.CYAN_BG = curses.color_pair(14)
        
    def _key_catch(self):
        self.poped = False
        self.PANBOX[self.pan_box].chgat(\
                        0, 0, 1, curses.A_REVERSE)
        while self.running:
            inp = self.RP.getch()
            #self.report('got: {}'.format(inp))
            if inp == 9 and not self.poped:  # tab
                try:  # slid out of screen
                    self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_NORMAL)
                except:
                    pass
                self.pan_box = (self.pan_box + 1) % (len(self.PANBOX))
                self.pan_loc[self.pan_box] = 0
                self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_REVERSE)
            elif inp == ord('h') and not self.poped:
                self.poped = True
                self.popup, self.popuppan, self._popup, self._popuppan =\
                        newpopup(25, 70, 3, 3, "Help", opts=self.CYAN_BG)
                self.disp(self.popup, PrintOut(HELP, opts=self.CYAN_BG))
                self.updpan()
            elif inp == 27 and self.poped:  # esc
                self.poped = False
                del self.popuppan
                del self.popup
                del self._popup
                del self._popuppan
                self.updpan()
            elif inp == curses.KEY_DOWN:
                try:  # slid out of screen
                    self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_NORMAL)
                except:
                    pass
                self.pan_loc[self.pan_box] += 1
                if not (0 <= self.pan_loc[self.pan_box]\
                                        < self.BOXSIZE[self.pan_box]):
                    self.pan_loc[self.pan_box] = self.BOXSIZE[self.pan_box]-1
                self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_REVERSE)
            elif inp == curses.KEY_UP:
                try:  # slid out of screen
                    self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_NORMAL)
                except:
                    pass
                self.pan_loc[self.pan_box] -= 1
                if not (0 <= self.pan_loc[self.pan_box]\
                                        < self.BOXSIZE[self.pan_box]):
                    self.pan_loc[self.pan_box] = 0
                self.PANBOX[self.pan_box].chgat(self.pan_loc[self.pan_box],
                                                0, 1, curses.A_REVERSE)
            elif inp == 339:  # PAGE UP
                self.PANBOX[self.pan_box].scroll(-1)
                #self.updpan()
            elif inp == 338:  # PAGE DOWN
                self.PANBOX[self.pan_box].scroll(1)
                #self.updpan()
            elif inp == ord('q') and not self.poped:
                self.poped = True
                self.popup, self.popuppan, self._popup, self._popuppan =\
                        newpopup(5, 60, 10, 3, "Preview", opts=self.CYAN_BG)
                self.disp(self.popup, PrintOut('hahaha', opts=self.CYAN_BG))
                self.updpan()
            #elif inp == ord('v'):
                #self.report(PrintOut(repr(self.pan_loc), newline=True))
            
            

                #self.running = False
            #self.RP.insertln()
            #self.RP.addstr(1, 0, "[" + s + "]")


def update_it(self):
    while self.running:
        # make local copy of list
        for win, item in list(self.printbuff):
            wd = self.PANBOX[win] if isinstance(win, int) else win
            if item.newline:
                wd.move(item.line, 0)
                wd.insertln()
                if isinstance(win, int):
                    self.pan_loc[win] += 1
            wd.addstr(item.line, item.col, item.text,
                            0 if item.opts is None else item.opts)
            self.printbuff.pop(0)
        
        self.updpan()
        time.sleep(1./PRINTFREQ)


def newpopup(h, w, y, x, title=None, line=True, opts=None):
    win, panel, wb, pn = newlinebox(h, w, y, x, title, line=line, opts=opts)
    if opts is not None:
        win.bkgd(" ", opts)
    panel.top()
    return win, panel, wb, pn


def newlinebox(h, w, y, x, title=None, line=True, opts=None):
    wb = curses.newwin(2, w, y-1, x)
    wb.keypad(True)
    if line:
        wb.addstr(0, 0, e(HORLINE)*w, 0 if opts is None else opts)
    if title is not None:
        wb.addstr(0, 2, e(title),  0 if opts is None else opts)
    pn = curses.panel.new_panel(wb)
    wb.refresh()
    win = curses.newwin(h, w, y, x)
    win.keypad(True)
    panel = curses.panel.new_panel(win)
    return win, panel, wb, pn


def loop_time(self):
    while self.running:
        self.set_time()
        time.sleep(1./TIMEUPDFREQ)


if not param_all.JUSTALIB:
    XDISP = Xdisp()
