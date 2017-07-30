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


from nanoctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from nanoctrl.ccsds.ccsdskey import CCSDSKey
from nanoctrl.ccsds.ccsdscategory import CCSDSCategory
from nanoctrl.utils import bincore
from nanoctrl.utils import b
from nanoctrl.utils import O


from . import param_category_common as cmn


__all__ = []


ACQMODESCIENCE = CCSDSKey(  name='acq_mode',
                            start=0*O,
                            l=1*O,
                            typ='uint',
                            verbose="Activates science mode (0=Searching, 1=Tracking, 2=Test). Valid for the entire packet.",
                            disp="mode")

INTEGRATIONTIME = CCSDSKey( name='integration_time',
                            start=1*O,
                            l=2*O,
                            typ='uint',
                            verbose="Integration time (valid for the entire packet). In ms/10.",
                            disp="itime")

DELAY = CCSDSKey(       name='delay',
                        start=3*O,
                        l=2*O,
                        typ='uint',
                        verbose="Delay between two integrations (in ms/10)",
                        disp="delay")

MODULATION = CCSDSKey(  name='modulation',
                        start=5*O,
                        l=1*O,
                        typ='uint',
                        verbose="Modulation pattern (0=Point, 1=Circle, 2=Flower, 3=Calibration pattern). Valid for the entire packet.",
                        disp="mod")

RADIUS = CCSDSKey(      name='radius',
                        start=6*O,
                        l=2*O,
                        typ='uint',
                        verbose="Radius of the modulation pattern. Valid for the entire packet.",
                        disp="rad")

NPOINTS = CCSDSKey(     name='n_points',
                        start=8*O,
                        l=1*O,
                        typ='uint',
                        verbose="Number of points in the pattern",
                        disp="npts")


HKTICK = CCSDSKey(          name='hk_tick',
                            start=0*O,
                            l=2*O,
                            typ='uint',
                            verbose="Sampling time for hk data (in ms). Valid for the entire packet.",
                            disp="hk_tick")

BINNING = CCSDSKey(         name='binning',
                            start=2*O,
                            l=1*O,
                            typ='uint',
                            verbose="Binning of the hk data (real sampling is thus binning*hkTick). Valid for the entire packet.",
                            disp="binning")

MAINMODE = CCSDSKey(        name='main_mode',
                            start=3*O,
                            l=1*O,
                            typ='uint',
                            verbose="Main mode of the payload (SBY = 0, IDL = 1, SCI = 2, IMG = 3, TST = 4). Valid for the entire packet.",
                            disp="mode")

ACQMODEHK = CCSDSKey(       name='acq_mode',
                            start=4*O,
                            l=1*O,
                            typ='uint',
                            verbose="mode for the acquisition manager. Valid for the entire packet.",
                            disp="acq_mode")

DIODEFLAG = CCSDSKey(       name='diode_flag',
                            start=5*O,
                            l=1*b,
                            typ='uint',
                            verbose="Is diode active?. Valid for the entire packet.",
                            disp="diode_flag")

INTERRUPTFLAG = CCSDSKey(   name='interrupt_flag',
                            start=41*b,
                            l=1*b,
                            typ='uint',
                            verbose="Is interrupt active?. Valid for the entire packet.",
                            disp="interrupt_flag")

PIEZOFLAG = CCSDSKey(       name='piezo_flag',
                            start=42*b,
                            l=1*b,
                            typ='uint',
                            verbose="Is piezo active?. Valid for the entire packet.",
                            disp="piezo_flag")

HVFLAG = CCSDSKey(          name='hv_flag',
                            start=43*b,
                            l=1*b,
                            typ='uint',
                            verbose="Is high-voltage line active?. Valid for the entire packet.",
                            disp="hv_flag")

SENSORSFLAG = CCSDSKey(     name='sensors_flag',
                            start=44*b,
                            l=1*b,
                            typ='uint',
                            verbose="Are strain gauges active?. Valid for the entire packet.",
                            disp="sensors_flag")

TECFLAG = CCSDSKey(         name='tec_flag',
                            start=45*b,
                            l=1*b,
                            typ='uint',
                            verbose="Is tec active?. Valid for the entire packet.",
                            disp="hv_flag")

BEACONFLAG = CCSDSKey(      name='beacon_flag',
                            start=46*b,
                            l=1*b,
                            typ='uint',
                            verbose="Is beacon active?. Valid for the entire packet.",
                            disp="beacon_flag")

PROCFREQ = CCSDSKey(        name='proc_freq',
                            start=6*O,
                            l=1*O,
                            typ='uint',
                            verbose="SYSCLOCK frequency (in MHz). Valid for the entire packet.",
                            disp="proc_freq")

TECSETPOINT = CCSDSKey(     name='tec_setpoint',
                            start=7*O,
                            l=2*O,
                            typ='uint',
                            verbose="Setpoint for the TEC controller (ADU). Valid for the entire packet.",
                            disp="tec_setpoint")


# HK payload
HEADAUX_4 = CCSDSTrousseau([HKTICK, BINNING, MAINMODE, ACQMODEHK, DIODEFLAG,
                                INTERRUPTFLAG, PIEZOFLAG, HVFLAG, SENSORSFLAG, TECFLAG,
                                BEACONFLAG, PROCFREQ, TECSETPOINT])
# science HF
HEADAUX_5 = CCSDSTrousseau([ACQMODESCIENCE, INTEGRATIONTIME, DELAY, MODULATION, RADIUS,
                                NPOINTS])


# (payloadd, category)
# no specific acknowledgement for payload
ACKCATEGORIESPLD = []


CATEGORIESPLD = {
                4: CCSDSCategory(name='payload HK',
                                 number=4,
                                 aux_trousseau=HEADAUX_4,
                                 data_file='param_payload_hk'),

                5: CCSDSCategory(name='HF science',
                                 number=5,
                                 aux_trousseau=HEADAUX_5,
                                 data_file='param_hf_science'),

                6: CCSDSCategory(name='pld report',
                                 number=6,
                                 aux_trousseau=None,
                                 data_file='param_pld_report'),

                7: CCSDSCategory(name='pld beacon',
                                 number=7,
                                 aux_trousseau=None,
                                 data_file='param_pld_beacon')
                        }

# extend all keys with common categories
CATEGORIESPLD.update(cmn.CATEGORIESCOMMON)


ACKCATEGORIESPLD += cmn.ACKCATEGORIESCOMMON
