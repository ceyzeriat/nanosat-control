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
from param import param_all
from param import param_apid
from param import param_commands
from byt import Byt

from . import core
from . import mgmtexception


__all__ = ['CommandList']


DISPSTRING = " #{:<3} L{:} PID {:<20} {:<30}  Np {:>2}  Lp {:>2}"


class CommandList(object):
    def __init__(self, cmds=None, autoLoad=True):
        """
        Manages the list of commands.

        Args:
          * cmds (str): the commands to manage: 'obc0', 'obc1', 'pld0',
            'pld1' or 'adcs'
          * autoLoad (bool): loads all the commands automatically
        """
        if cmds not in param_commands.COMMANDSFILE.keys():
            print("Unknow cmds type, should be in {}"\
                        .format(list(param_commands.COMMANDSFILE.keys())))
        else:
            self._cmds = cmds
            if autoLoad:
                self.loadCMDS()

    def __str__(self):
        txt = ["Commands of {}".format(self._cmds)]
        txt.append("{:d} commands".format(len(self.allcmds)))
        for item in self.allcmds:
            txt.append(DISPSTRING.format(
                        item['number'],
                        param_apid.LVLREGISTRATION.get(item['pid'], '?'),
                        item['pid'],
                        item['name'],
                        len(item['param']),
                        item['lparam'] if item['lparam'] is not None else "*"))
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
        self.allcmds = [dict(item)\
                            for item in core.load_json_cmds(
                                param_commands.COMMANDSFILE[self._cmds])]
        print("Loaded {:d} commands from {}".format(len(self.allcmds),
                                                    self._cmds))

    def remove(self, number):
        """
        Deletes one or several commands

        Args:
          * number (int or list of int): the id of the command(s) to remove

        Changes shall be saved using apply method.
        """
        if not hasattr(number, '__iter__'):
            number = [number]
        for num in number:
            for idx, item in enumerate(self.allcmds):
                if item['number'] == num:
                    dum = self.allcmds.pop(idx)
                    print("Removed:\n{}".format(dum))
            else:
                print("Didn't find command #'{}'".format(num))

    def remove_all(self):
        """
        Deletes all commands. Changes shall be saved using ``apply``.
        """
        self.allcmds = []

    def loadCSV(self, filename, titles_row, delimiter='#'):
        """
        Loads the csv import-file

        Args:
          * filename (str): the path+file of the CSV
          * titles_row (int): the number of lines to skip at the top of
            CSV file
          * delimiter (char): the CSV delimiter, no kidding
        """
        csvcontent = csv.reader(open(str(filename)),
                                delimiter=str(delimiter)[0])
        # skip the shit
        for l in range(int(titles_row)):
            next(csvcontent)
        self.csvcontent = self._grabCSV(csvcontent)
        print("Loaded {:d} commands".format(len(self.csvcontent)))

    def _grabCSV(self, itera):
        ll = []
        cm = None
        for line in itera:
            # is empty line ?
            if line[param_commands.CSVNAME] == "" and\
                        line[param_commands.CSVPARAMNAME] == "":
                continue
            # that's a new command, not an additional parameter
            if line[param_commands.CSVSUBSYSTEM] != "":
                if cm is not None:
                    ll.append(cm)
                cm = {
                    'number': int(line[param_commands.CSVNUMBER]),
                    'name':\
                        core.rchop(core.ustr(line[param_commands.CSVNAME])\
                                        .replace(' ', '_'), '_TM'),
                    'pid': core.ustr(line[param_commands.CSVPID]).lower(),
                    'desc': core.ustr(line[param_commands.CSVDESC]),
                    'lparam':\
                        int(0\
                            if line[param_commands.CSVLPARAM].strip() == ""\
                            else line[param_commands.CSVLPARAM])\
                        if line[param_commands.CSVLPARAM].strip() != "*"\
                        else "*",
                    'subsystem':\
                        core.ustr(line[param_commands.CSVSUBSYSTEM])\
                                                .lower().replace(' ', '_'),
                    'param': [],
                    'n_nparam':\
                        int(line[param_commands.CSVNPARAM]\
                        if line[param_commands.CSVNPARAM].strip() != ""\
                                else 0)}
                # adcs specific stuff
                if self._cmds == 'adcs':
                    cm.update({
                        'subSystemKey': Byt(int(line[\
                            param_commands.CSVSUBSYSTEMKEYADCS]\
                            .strip(), 16))[0].hex(),
                        'adcsCommandId': Byt(int(line[\
                            param_commands.CSVCOMMANDIDADCS]\
                            .strip(), 16))[0].hex()})
            # no parameter command
            if cm['n_nparam'] == 0:
                cm['lparam'] = 0
            else:  # adding parameters to the last command added
                cm['param'].append([
                        core.ustr(line[param_commands.CSVPARAMNAME])\
                                            .replace(' ', '_'),
                        core.ustr(line[param_commands.CSVPARAMDESC]),
                        core.ustr(line[param_commands.CSVPARAMRNG]),
                        core.ustr(line[param_commands.CSVPARAMTYP])\
                                            .replace('_t', ''),
                        core.ustr(line[param_commands.CSVPARAMSIZE]),
                        core.ustr(line[param_commands.CSVPARAMUNIT])\
                                            .replace(' ', '_')])
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
            print(DISPSTRING.format(
                    item['number'],
                    param_apid.LVLREGISTRATION.get(item['pid'], '?'),
                    item['pid'],
                    item['name'],
                    len(item['param']),
                    item['lparam'] if item['lparam'] is not None else "*"))
            if item['pid'] not in param_apid.PIDREGISTRATION.keys():
                print("!!!! Issue, PID is unknown (case sensitive)")
            lvl = str(param_apid.LVLREGISTRATION.get(item['pid'], '?'))[0]
            if self._cmds[-1] != lvl and self._cmds != 'adcs':
                print("!!!! Issue, LVL doesn't match cmds file")
            if core.clean_name(item['name']) != item['name']:
                print("!!!! Issue, your name is not code friendly")
            if len(item['param']) != item['n_nparam']:
                print("!!!! Issue, length of param is different from lparam")
            for itemp in item['param']:
                if len(itemp[0]) > param_commands.LENPARAMNAME:
                    print("!!!! Issue, param name is too long")
                if core.clean_name(itemp[0]) != itemp[0]:
                    print("!!!! Issue, param name is not code friendly")

    def new_fromCSV(self, ids):
        """
        Adds one or several commands to the file

        Args:
          * ids (int or list of ints): the ids of the new command(s) to add
            from the CSV.
        
        Changes shall be saved using apply method.
        """
        if not hasattr(self, 'csvcontent'):
            print("Please load the CSV first")
            return
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        allids = [item['number'] for item in self.allcmds]
        allnames = [item['name'].lower() for item in self.allcmds]
        to_add = []
        cnt = 0
        for item in self.csvcontent:
            if item['number'] in ids:
                if item['number'] in allids\
                            or item['name'].lower() in allnames:
                    raise mgmtexception.RedundantCm(i=item['number'],
                                                    n=item['name'])
                copyitem = dict(item)
                # we do not save n_nparam
                copyitem.pop('n_nparam')
                to_add.append(copyitem)
                cnt += 1
                allids.append(item['number'])
                allnames.append(item['name'])
        else:
            if cnt > 0:
                print('You shall add these new commands to the database with:')
            for item in to_add:
                print("INSERT INTO commands VALUES ({:d}, '{}');".format(\
                            item['number'], item['name']))
            self.allcmds += to_add
            print("Added {:d} commands from CSV".format(cnt))

    def update_fromCSV(self, ids):
        """
        Adds one or several commands to the file

        Args:
          * ids (int or list of ints): the ids of the command(s) to update
            from the CSV.
        
        Changes shall be saved using apply method.
        """
        if not hasattr(self, 'csvcontent'):
            print("Please load the CSV first")
            return
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        allids = [item['number'] for item in self.allcmds]
        to_upd = []
        cnt = 0
        for item in self.csvcontent:
            if item['number'] in ids:
                if item['number'] not in allids:
                    raise mgmtexception.MissinfCm(i=item['number'])
                copyitem = dict(item)
                # we do not save n_nparam
                copyitem.pop('n_nparam')
                to_upd.append(copyitem)
                cnt += 1
                allids.append(item['number'])
        else:
            if cnt > 0:
                print('You shall update these commands in the database with:')
            # for each cmd to update
            for cmd in to_upd:
                print("UPDATE commands SET name='{}' WHERE id={};".format(\
                            cmd['name'], cmd['number']))
                # scan the loaded commands to remove it
                for idx, v in enumerate(self.allcmds):
                    if v['number'] == cmd['number']:
                        self.allcmds.pop(idx)
            self.allcmds += to_upd
            print("Updated {:d} commands from CSV".format(cnt))
            print("\nWARNING: Updating a command might corrupt the TC/TM"\
                  "data previously recorded in the database")

    def apply(self):
        """
        Applies the add/update/remove changes to the JSON files
        """
        core.save_json_cmds(param_commands.COMMANDSFILE[self._cmds],
                            cmds=self.allcmds)
        print("Saved {:d} commands to {} file".format(len(self.allcmds),
                                                      self._cmds))
