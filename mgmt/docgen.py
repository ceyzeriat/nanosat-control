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


from pylatex import Document, Section, Subsection, Tabular, NoEscape,\
                        Command, Itemize, MultiColumn, Subsubsection
from pylatex.basic import NewLine
from pylatex.utils import italic
from ctrl.ccsds import param_ccsds
import param
import os
import re


__all__ = ['DocGen']


class DocGen(object):
    def __init__(self, docname):
        """
        Generates the pdf for PicSat communication specifications

        Args:
          * docname (str): the name of the pdf document generated
            optionnally with the path (default is "here")

        Method:
          * generate: use it to generate the document
        """
        docname = str(docname)
        if docname.lower().endswith('.tex'):
            docname = docname[:-4]
        self.docname = docname

    def generate(self, clean_tex=True):
        """
        Generates the document and saves it to disk

        Args:
          * clean_tex (bool): whether to delete the .tex file after
            compiling
        """
        doc = Document(self.docname)
        doc.preamble.append(Command('usepackage', 'hyperref'))
        doc.preamble.append(Command('title',
                                    'PicSat Communication Specifications'))
        doc.preamble.append(Command('author', 'Python et al.'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))
        doc.append(NoEscape(r'\tableofcontents'))
        # Telecommands
        section = Section('Telecommands')
        subsection = self._trousseau2subsection('Primary Header',
                                        param_ccsds.HEADER_P_KEYS)
        section.append(subsection)
        subsection = self._trousseau2subsection('Secondary Header',
                                        param_ccsds.HEADER_S_KEYS_TELECOMMAND)
        section.append(subsection)
        subsection = self._TCauxHeader()
        section.append(subsection)
        doc.append(section)
        # Telemetries
        section = Section('Telemetries')
        subsection = self._trousseau2subsection('Primary Header',
                                        param_ccsds.HEADER_P_KEYS)
        section.append(subsection)
        subsection = self._trousseau2subsection('Secondary Header',
                                        param_ccsds.HEADER_S_KEYS_TELEMETRY)
        section.append(subsection)
        subsection = self._TMauxHeader()
        section.append(subsection)
        doc.append(section)
        # Packet Categories
        sectionname = {0: 'Packet Categories OBC',
                       1: 'Packet Categories Payload'}
        for idx, pldflag in ([0, False], [1, True]):
            section = Section(sectionname[idx])
            for catnum, cat in param.param_category.\
                                    PACKETCATEGORIES[idx].items():
                subsection = self._trousseau2subsection(
                    '{} ({:d}) - Auxiliary Header'.format(cat.name, catnum),
                    cat, catnum=catnum, pldflag=pldflag)
                section.append(subsection)
                cat_params = param.param_category.FILEDATACRUNCHING[\
                                                            idx][catnum]
                if cat_params is None:  # no specifics for unpacking data
                    dat = None
                else:
                    dat = getattr(param, cat_params).TROUSSEAU
                subsection = self._trousseau2subsection(
                            '{} ({:d}) - Data'.format(cat.name, catnum),
                            dat, catnum=catnum, pldflag=False)
                section.append(subsection)
            doc.append(section)
        self._compile(doc, clean_tex=False)

    def _compile(self, doc, clean_tex=False):
        """
        Just compile the doc and save to disk

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

    def _TCauxHeader(self):
        """
        Fills the axu header section for TC
        """
        subsection = Subsection('Auxiliary Header and Data')
        subsection.append("No auxiliary header.")
        subsection.append(NewLine())
        subsection.append("The data field is the "\
                          "octet-concatenation of telecommand input "\
                          "parameters, as per telecommands documentation.")
        return subsection

    def _TMauxHeader(self):
        """
        Fills the axu header section for TM
        """
        subsection = Subsection('Auxiliary Header and Data')
        subsection.append("The auxiliary header and data fields definitions "\
                          "depend on the payload flag and the packet "\
                          "category.")
        subsection.append(NewLine())
        subsection.append("Refer to Sections Packet Category OBC and Payload")
        return subsection

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
        subsection = Subsection(str(subname))
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
            res = [r"Total size (octets): {}".format(T.size), NewLine(),
                   r"Keys count: {}".format(len(T.keys)), NewLine(),
                   r"To be treated as octets: {}".format(str(T.octets)),
                   NewLine(), NewLine()]
            if T.listof:
                res += [r"NB: The keys-structure presented below is "\
                        r"repeated N-times in the packet.",
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
            if not cle.relative_only:
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
            start_bit += cle.len
        return res

