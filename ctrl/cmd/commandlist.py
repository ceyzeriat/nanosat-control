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


import csv
from param import param_apid
from . import cmdexception
from . import param_commands
from .command import Command
from ..utils import core


__all__ = ['CommandList']


class CommandList(object):
    def __init__(self, ):
        """
        Manages the list of commands.

        Args:
        * filename (str): the absolute or relative path to the .csv
            import file.
        * titles_row (int): the row index (starting 0) of the titles in
            the csv. The first data row is expected to be on the following
            row.
        """
        self.loadCMDS()

    def __str__(self):
        txt = ["{:d} commands".format(len(self.allcmds))]
        for item in self.allcmds:
            txt.append(" #{:<3} L{} {:<25}  Np {}  Lp {}".format(
                            item.number,
                            int(item.level),
                            item.name,
                            item.nparam,
                            item.lparam if item.lparam is not None else "*"))
        return "\n".join(txt)

    __repr__ = __str__

    def show(self):
        """
        Shows the available commands. Save changes using ``apply``
        """
        print(self)

    def loadCMDS(self):
        """
        Loads all the commands from the JSON file. Changes not applied
        will be lost
        """
        self.allcmds = [Command(**item)\
                for item in core.load_json_cmds(param_commands.COMMANDSFILE)]
        print("Loaded {:d} commands".format(len(self.allcmds)))

    def remove(self, number):
        """
        Deletes the command ``number`` from the list. Changes shall be
        saved using ``apply``.
        """
        for idx, item in enumerate(self.allcmds):
            if item.number == number:
                dum = self.allcmds.pop(idx)
                print("Removed:\n{}".format(dum))
                break
        else:
            print("Didn't find command number '{}'".format(number))

    def remove_all(self):
        """
        Deletes all commands. Changes shall be saved using ``apply``.
        """
        self.allcmds = []

    def loadCSV(self, filename, titles_row=0, delimiter='#'):
        """
        Loads the csv import-file
        """
        csvcontent = csv.reader(open(str(filename)),
                                delimiter=str(delimiter)[0])
        # skip the shit
        for l in range(int(titles_row)):
            self.csvcontent.next()
        self.titles = csvcontent.next()
        self.csvcontent = self._grabCSV(csvcontent)
        print("Loaded {:d} commands".format(len(self.csvcontent)))

    def _grabCSV(self, itera):
        ll = []
        cm = None
        for line in itera:
            # that's a new command, not an additional parameter
            if line[param_commands.CSVSUBSYSTEM] != "":
                if cm is not None:
                    ll.append(cm)
                cm = {'number': int(line[param_commands.CSVNUMBER]),
                        'name': _rchop(str(line[param_commands.CSVNAME])\
                                        .strip().replace(' ', '_'), '_TM'),
                        'pid': str(line[param_commands.CSVPID]).strip(),
                        'desc': str(line[param_commands.CSVDESC]).strip(),
                        'lparam':\
                        int(0 if line[param_commands.CSVLPARAM].strip() == ""
                                else line[param_commands.CSVLPARAM])\
                        if line[param_commands.CSVLPARAM].strip() != "*"
                            else "*",
                        'subsystem': str(line[param_commands.CSVSUBSYSTEM])\
                                                .lower().replace(' ', '_'),
                        'param': [],
                        'n_nparam': int(line[param_commands.CSVNPARAM]\
                            if line[param_commands.CSVNPARAM].strip() != ""\
                                else 0)}
            # no parameter command
            if cm['n_nparam'] == 0:
                cm['lparam'] = 0
            else:  # adding parameters to the last command added
                cm['param'].append([str(line[param_commands.CSVPARAMNAME])\
                                                .strip().replace(' ', '_'),
                                    str(line[param_commands.CSVPARAMDESC])\
                                                .strip(),
                                    str(line[param_commands.CSVPARAMRNG])\
                                                .strip(),
                                    str(line[param_commands.CSVPARAMTYP])\
                                        .strip().replace('_t', ''),
                                    str(line[param_commands.CSVPARAMSIZE])\
                                        .strip(),
                                    str(line[param_commands.CSVPARAMUNIT])\
                                        .strip().replace(' ', '_')])
        ll.append(cm)
        return ll

    def showCSV(self):
        """
        Shows the content of the CSV
        """
        if not hasattr(self, 'csvcontent'):
            print("Please load the CSV first")
            return
        print("{:d} commands in the CSV".format(len(self.csvcontent)))
        for item in self.csvcontent:
            print(" #{:<3} PID {:<20} {:<25}  Np {}  Lp {}".format(
                    item['number'],
                    item['pid'],
                    item['name'],
                    len(item['param']),
                    item['lparam'] if item['lparam'] is not None else "*"))
            if item['pid'] not in param_apid.PIDREGISTRATION.keys():
                print("!!!! Issue, PID is unknown (case sensitive)")
            if core.clean_name(item['name']) != item['name']:
                print("!!!! Issue, your name is not code friendly")
            if len(item['param']) != item['n_nparam']:
                print("!!!! Issue, length of param is different from lparam")
            for itemp in item['param']:
                if len(itemp[0]) > param_commands.LENPARAMNAME:
                    print("!!!! Issue, param name is too long")
                if core.clean_name(itemp[0]) != itemp[0]:
                    print("!!!! Issue, param name is not code friendly")

    def addCSV(self, ids_to_add=[]):
        """
        Adds the commands from the list ``ids_to_add`` from the CSV.
        Changes shall be saved using ``apply``.
        """
        if not hasattr(self, 'csvcontent'):
            print("Please load the CSV first")
            return
        allids = [item.number for item in self.allcmds]
        allnames = [item.name.lower() for item in self.allcmds]
        to_add = []
        cnt = 0
        for item in self.csvcontent:
            if item['number'] in ids_to_add:
                if item['number'] in allids\
                            or item['name'].lower() in allnames:
                    raise cmdexception.RedundantCm(i=item['number'],
                                                   n=item['name'])
                copyitem = dict(item)
                copyitem.pop('n_nparam')
                to_add.append(Command(**copyitem))
                cnt += 1
                allids.append(item['number'])
                allnames.append(item['name'])
        else:
            self.allcmds += to_add
            print("Added {:d} commands from CSV".format(cnt))

    def apply(self):
        """
        Applies the add/remove changes to the JSON file
        """
        core.save_json_cmds(param_commands.COMMANDSFILE,
                            cmds=[item.to_dict() for item in self.allcmds])
        print("Saved {:d} commands".format(len(self.allcmds)))

def _rchop(txt, ending):
    if txt.lower().endswith(ending.lower()):
        return txt[:-len(ending)]
    else:
        return txt
