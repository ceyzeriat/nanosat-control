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
#.path
###############################################################################


from pylatex import Document, Section, Subsection, Tabular, NoEscape,\
                        Command, Itemize, MultiColumn, Subsubsection
from pylatex.basic import NewLine
from pylatex.utils import italic
from nanoctrl.cmd import allcommand
from nanoparam.categories import param_tc_answer
from nanoparam import param_all_processed as param_all
import os
import re


__all__ = ['DocTCTM']


DOCNAME = "PICSAT-TCTM-SPEC-01"
REPL = {"<!SHORTTITLE!>": 'PicSat Comm. Spec.',
        "<!VERSION!>": '1.0',
        "<!STITLE!>": 'PicSat TC-TM Specifications',
        "<!PATH!>": param_all.Pathing('ctrl', 'mgmt').path,
        "<!REF!>": DOCNAME}


class DocTCTM(object):
    def __init__(self):
        """
        Generates the pdf for PicSat communication specifications

        Args:
          * docname (str): the name of the pdf document generated
            optionnally with the path (default is "here")

        Method:
          * generate: use it to generate the document
        """
        self.docname = DOCNAME

    def generate(self, clean_tex=True):
        """
        Generates the document and saves it to disk

        Args:
          * clean_tex (bool): whether to delete the .tex file after
            compiling
        """
        HEADER = open(param_all.Pathing('ctrl', 'mgmt', 'header.tex').path, mode='r').read()
        HEADER2 = open(param_all.Pathing('ctrl', 'mgmt', 'header-2.tex').path, mode='r').read()
        doc = Document(self.docname)
        for k, v in REPL.items():
            HEADER = HEADER.replace(k, v)
            HEADER2 = HEADER2.replace(k, v)
        doc.preamble.append(NoEscape(HEADER))
        doc.append(NoEscape(HEADER2))
        section = Section('Principles')
        section.append(
"""The Telecommand (TC) and Telemetry (TM) packets format specifications are based on the CCSDS format: the concatenation of a primary header, secondary header, (optional) auxiliary header, (optional) data field.

TC are composed of a 6 octets primary header and a 18 octets secondary header. There is no auxiliary header. The data field contains values which depend on the command ID, that are treated by the satelite as input parameters.

TM are composed of a 6 octets primary header and a 6 octets secondary header. The TM category defines what type of TM is transmitted (e.g. beacon, house keeping) and how the auxiliary header and data field are encoded.

This documents covers the content of data field for TC, and the content of auxiliary header and data fields for the TM category 'TC Answer'.

This document does not cover the content of headers for TC, and headers and data fields for TM. This information is available in the dedicated communication specifications document.""")
        doc.append(section)
        # Telecommands
        section = Section('Commands for OBC-L0')
        for item in list(sorted(allcommand.L0CMDS, key=lambda x: x.number)):
            subsection = Subsection('#{:d}: {}'.format(item.number, item.name))
            subsection.append(self._print_TC(item))
            section.append(subsection)
            # add TM if need be
            if item.number in param_tc_answer.TROUSSEAUDIC.keys():
                subsection = self._trousseau2subsection("Answer TM to {}".format(item.name),
                                        param_tc_answer.TROUSSEAUDIC[item.number])
                section.append(subsection)
        doc.append(section)

        section = Section('Commands for OBC-L1')
        for item in list(sorted(allcommand.L1OBCCMDS, key=lambda x: x.number)):
            subsection = Subsection(item.name)
            subsection.append(self._print_TC(item))
            section.append(subsection)
            # add TM if need be
            if item.number in param_tc_answer.TROUSSEAUDIC.keys():
                subsection = self._trousseau2subsection("Answer TM to {}".format(item.name),
                                        param_tc_answer.TROUSSEAUDIC[item.number])
                section.append(subsection)
        doc.append(section)

        section = Section('Commands for PLD-L1')
        for item in list(sorted(allcommand.L1PLDCMDS, key=lambda x: x.number)):
            subsection = Subsection(item.name)
            subsection.append(self._print_TC(item))
            section.append(subsection)
            # add TM if need be
            if item.number in param_tc_answer.TROUSSEAUDIC.keys():
                subsection = self._trousseau2subsection("Answer TM to {}".format(item.name),
                                        param_tc_answer.TROUSSEAUDIC[item.number])
                section.append(subsection)
        doc.append(section)
        self._compile(doc, clean_tex=clean_tex)


    def _print_TC(self, TC):
        return "#{} {} (L{}, pid: {})\n {}\n{} params: ({} octet)\n{}".format(
                            TC.number,
                            TC.name,
                            int(TC.level),
                            TC._pidstr,
                            TC.desc,
                            TC.nparam,
                            TC.lparam if TC.lparam is not None else "*",
                            "\n".join([str(item) for item in TC._params]))

    def _compile(self, doc, clean_tex=True):
        """
        Compiles the doc and saves to disk

        Args:
          * doc (pylatex Document): the document to compile
          * clean_tex (bool): whether to delete the .tex file after
            compiling
        """
        # Triple compilation, just because latex is awesome
        doc.generate_pdf(self.docname, clean=False, clean_tex=False,
                         compiler='pdflatex')
        doc.generate_pdf(self.docname, clean=False, clean_tex=False,
                         compiler='pdflatex')
        doc.generate_pdf(self.docname, clean=True, clean_tex=bool(clean_tex),
                         compiler='pdflatex')
        if os.path.isfile(self.docname + ".toc"):
            os.remove(self.docname + ".toc")

    def _trousseau2subsection(self, subname, T, catnum=None, pldflag=None):
        """
        Takes a whole trousseau and generates the document latex for it

        Args:
          * subname (str): name of the subsection
          * T (trousseau): the trousseau to generate code on
          * catnum (None, int): None if the trousseau is not a
            category, or the category number
          * pldflag (None, bool): None if the trousseau is not a
            category, or bool corresponding to the payload flag
        """
        subsection = Subsection(str(subname), numbering=False)
        if catnum is not None:
            subsection.append('Payload flag: {}'.format(pldflag))
            subsection.append(NewLine())
            subsection.append('Packet Category number: {:d}'.format(catnum))
            subsection.append(NewLine())
        desc = self._trousseau2desc(T)
        for item in desc:
            subsection.append(item)
        table = self._trousseau2table(T)
        for item in table:
            subsection.append(item)
        detail = self._trousseau2allfields(T)
        for item in detail:
            subsection.append(item)
        return subsection

    def _trousseau2desc(self, T):
        """
        Generates latex code for the general content of the trousseau

        Args:
          * T (trousseau): the trousseau to generate code on
        """
        if T is None or getattr(T, 'size', 0) == 0:
            return [r"Total size (octets): 0", NewLine()]
        else:
            Ns = " x N" if T.listof else ""
            res = [r"Total size (octets): {}{}".format(T.size, Ns), NewLine(),
                   r"Keys count: {}{}".format(len(T.keys), Ns), NewLine(),
                   r"To be treated as octets: {}".format(str(T.octets)),
                   NewLine(), NewLine()]
            if T.listof:
                res += [r"NB: The keys-structure presented below is "\
                        r"repeated N times up to the total size.",
                        NewLine(), NewLine()]
            return res

    def _subtable(self, idx, subK, octets):
        """
        Generates latex code for a ccsds keys table

        Args:
          * idx (int): the index of the current sub-table in case the
            trousseau needs to be split into several tables
          * subK (list of keys): the list of keys to generate table on
          * octets (bool): corresponding to trousseau.octets
        """
        titles = ('Name', 'Start', 'Len', 'Value')
        table = Tabular('|'.join(['l'] + ['c']*(len(titles)-1)))
        if idx > 0:
            table.add_row((MultiColumn(len(titles), align='c',
                                   data=italic("Continued")),))
        table.add_row(titles)
        unit = "octets" if octets else "bits"
        table.add_hline()
        table.add_hline()
        start_bit = 0
        for cle in subK:
            if not cle.relative_only:
                start_bit = cle.start
            # if no padding, allows flexible len of the ccsdskey
            the_len = cle.len if cle.pad else "[0..{:d}]".format(cle.len)
            if cle.isdic:
                if cle.dic_force is not None:
                    the_type = repr(cle.dic[cle.dic_force])
                else:
                    the_type = repr(cle.dic.values())
            else:
                the_type = re.search(r'type *= *([\S ]+)',
                                     getattr(cle._fctunpack, 'func_doc', ''))
                if the_type is None:
                    the_type = '-'
                else:
                    the_type = the_type.group(1)
            table.add_row((cle.name, start_bit, the_len, the_type))
            start_bit += cle.len
        table.add_row((MultiColumn(len(titles), align='c',
                                   data='"Start" and "Len" are given in {}'\
                                        .format(unit)),))
        return table

    def _trousseau2table(self, T, sort_it=True, split_table=35):
        """
        Generates latex code for one or several (if too large) tables
        of ccsds keys

        Args:
          * T (trousseau): the trousseau to generate code on
          * sort_it (bool): whether to re-order the keys using their
            start values
          * split_table (int): maximum amount of keys to display on a
            single table
        """
        if T is None or getattr(T, 'size', 0) == 0:
            return []
        if sort_it:
            Tkeys = sorted(T.keys, key=lambda x: x.start)
        else:
            Tkeys = T.keys
        table = []
        for idx, bit in enumerate(range(0, len(Tkeys), split_table)):
            table.append(self._subtable(idx,
                                        Tkeys[bit:bit+split_table],
                                        T.octets))
            table.append(NewLine())
            table.append(NewLine())
        return table

    def _trousseau2allfields(self, T, sort_it=True):
        """
        Generates latex code for the verbose of a list of ccsds keys

        Args:
          * T (trousseau): the trousseau to generate code on
          * sort_it (bool): whether to re-order the keys using their
            start values
        """
        if T is None or getattr(T, 'size', 0) == 0:
            return []
        unit = "octet" if T.octets else "bit"
        if sort_it:
            Tkeys = sorted(T.keys, key=lambda x: x.start)
        else:
            Tkeys = T.keys
        res = []
        start_bit = 0
        for cle in Tkeys:
            clesection = Subsubsection(cle.name)
            items = []
            start_bit = cle.start
            # if no padding, allows flexible len of the ccsdskey
            the_len = cle.len if cle.pad else "[0..{:d}]".format(cle.len)
            if cle.isdic:
                the_verbose = "N/A"
                if cle.dic_force is not None:
                    the_type = repr(cle.dic[cle.dic_force])
                else:
                    the_type = repr(cle.dic.values())
            else:
                the_type = re.search(r'type *= *([\S ]+)',
                                     getattr(cle._fctunpack, 'func_doc', ''))
                the_verbose = re.search(r'verbose *= *([\S ]+)',
                                     getattr(cle._fctunpack, 'func_doc', ''))
                if the_type is None:
                    the_type = '-'
                else:
                    the_type = the_type.group(1)
                if the_verbose is None:
                    the_verbose = "N/A"
                else:
                    the_verbose = the_verbose.group(1)
            items += [r"{}".format(cle.verbose),
                    r"Start {}: {}, length ({}s): {}, value: {}"\
                        .format(unit, start_bit, unit, the_len, the_type),
                    r"Conversion: {}".format(the_verbose)]
            if cle.name != cle.disp:
                items += ["Shortened as '{}'".format(cle.disp)]
            for item in items:
                clesection.append(item)
                clesection.append(NewLine())
            res.append(clesection)
        return res

