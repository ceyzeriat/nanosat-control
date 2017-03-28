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


from sys import version_info
PYTHON3 = version_info > (3,)

import os
import json
from param import params
from byt import Byt


# make sure that python 3 understands unicode native python 2 function
if PYTHON3:
    unicode = str

def load_json_cmds(path):
    """
    Loads all the commands from the json file, given the path list
    """
    f = open(params.rel_dir(*path), mode='r')
    allcmds = json.load(f)
    f.close()
    return allcmds

def rchop(txt, ending):
    """
    Removes ``ending`` at the end of ``txt`` and returns the shortened string
    """
    if txt.lower().endswith(ending.lower()):
        return txt[:-len(ending)]
    else:
        return txt

def clean_name(txt):
    """
    Cleans the ``txt`` from non-alphanum characters; replaces the first
    character by a word if it is a number
    """
    if not isinstance(txt, (str, unicode)):
        raise TypeError("txt must be string or unicode")
    number = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
              "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    authorized = list(range(65, 91)) + list(range(97, 123))\
                    + list(range(48, 58)) + [95]
    txt = "".join([letter for letter in str(txt)
                        if (ord(letter) in authorized)])
    return number[txt[0]] + "_" if ord(txt[0]) in number.keys() else txt[0]\
            + txt[1:]

def save_json_cmds(path, cmds):
    """
    Saves all the commands from the json file, given the path and
    the commands list
    """
    f = open(params.rel_dir(*path), mode='w')
    json.dump(cmds, f)
    f.close()

def ustr(txt):
    """
    Returns an ASCII cleaned version of the text
    """
    return ''.join([ch for ch in txt.encode('utf-8')\
                    if 32 <= ord(ch) <= 127]).strip()
