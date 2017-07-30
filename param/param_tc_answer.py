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


from ctrl.ccsds.ccsdsmetatrousseau import CCSDSMetaTrousseau
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


__all__ = ['TROUSSEAU']


TROUSSEAUDIC = {1: CCSDSTrousseau([CCSDSKey(name='message', start=0*O, l=10*O, typ='byt', verbose='none', disp='message',)]),
                4: CCSDSTrousseau([CCSDSKey(name='time', start=0*O, l=4*O, typ='uint', verbose='none', disp='time',)]),
                5: CCSDSTrousseau([CCSDSKey(name='time', start=0*O, l=4*O, typ='uint', verbose='none', disp='time',)]),
                6: CCSDSTrousseau([CCSDSKey(name='count', start=0*O, l=2*O, typ='uint', verbose='none', disp='count',)]),
                7: CCSDSTrousseau([CCSDSKey(name='temp1', start=0*O, l=2*O, typ='sint', verbose='none', disp='temp1',),
                                   CCSDSKey(name='temp2', start=2*O, l=2*O, typ='sint', verbose='none', disp='temp2',),
                                   CCSDSKey(name='temp3', start=4*O, l=2*O, typ='sint', verbose='none', disp='temp3',),
                                   CCSDSKey(name='temp4', start=6*O, l=2*O, typ='sint', verbose='none', disp='temp4',),
                                   CCSDSKey(name='temp5', start=8*O, l=2*O, typ='sint', verbose='none', disp='temp5',)]),
                11: CCSDSTrousseau([CCSDSKey(name='data', start=0*O, l=255*O, typ='byt', verbose='none', disp='data', hard_l=False)]),
                17: CCSDSTrousseau([CCSDSKey(name='data', start=0*O, l=255*O, typ='byt', verbose='none', disp='data', hard_l=False)]),
                17: CCSDSTrousseau([CCSDSKey(name='data', start=0*O, l=255*O, typ='byt', verbose='none', disp='data', hard_l=False)]),
                48: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                49: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                50: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                51: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                52: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                55: CCSDSTrousseau([CCSDSKey(name='crc', start=0*O, l=4*O, typ='byt', verbose='none', disp='crc',)]),
                63: CCSDSTrousseau([CCSDSKey(name='patchState', start=0*O, l=1*O, typ='uint', verbose='none', disp='patchState',)]),
                81: CCSDSTrousseau([CCSDSKey(name='i2cReply', start=0*O, l=255*O, typ='byt', verbose='none', disp='i2cReply', hard_l=False)]),
                82: CCSDSTrousseau([CCSDSKey(name='adcsMode', start=0*O, l=4*O, typ='uint', verbose='none', disp='adcsMode',)]),


#PAYLOAD BOOTLOADER
                200: CCSDSTrousseau([CCSDSKey(name='version', start=0*O, l=255*O, typ='text', verbose='none', disp='version', hard_l=False)]),
                246: CCSDSTrousseau([CCSDSKey(name='values', start=0*O, l=255*O, typ='hexstr', verbose='none', disp='values', hard_l=False)]),
                248: CCSDSTrousseau([CCSDSKey(name='message', start=0*O, l=255*O, typ='hexstr', verbose='none', disp='msg', hard_l=False)]),
                250: CCSDSTrousseau([CCSDSKey(name='flashBytes', start=0*O, l=255*O, typ='hexstr', verbose='none', disp='flashBytes', hard_l=False)]),

#L1 OBC
                300: CCSDSTrousseau([CCSDSKey(name='messa', start=0*O, l=10*O, typ='byt', verbose='none', disp='message',)]),
                305: CCSDSTrousseau([CCSDSKey(name='TimerProc', start=0*O, l=1*O,  typ='uint', verbose='Timer for data processing', disp='TimerProc',unit='s'),
                                     CCSDSKey(name='TimerL1Hk', start=1*O, l=1*O,  typ='uint', verbose='Timer for hkL1 retrieval', disp='TimerHk',unit='s'),
                                     CCSDSKey(name='hkStandardPeriod', start=2*O, l=1*O,  typ='uint', verbose='Period of ADCS fetch of standard Hk', disp='standard',unit='ticks'),
                                     CCSDSKey(name='hkActuatorPeriod', start=3*O, l=1*O,  typ='uint', verbose='Period of ADCS fetch of actuator Hk', disp='actuator',unit='ticks'),
                                     CCSDSKey(name='hkSensorPeriod', start=4*O, l=1*O,  typ='uint', verbose='Period of ADCS fetch of sensor Hk', disp='sensor',unit='ticks'),
                                     CCSDSKey(name='hkAttitudePeriod', start=5*O, l=1*O,  typ='uint', verbose='Period of ADCS fetch of attitude Hk', disp='attitude',unit='ticks'),
                                     CCSDSKey(name='hkL1OBCPeriod', start=6*O, l=1*O,  typ='uint', verbose='Period of fetch of L1 Hk', disp='l1Hk',unit='ticks')]),
                307: CCSDSTrousseau([CCSDSKey(name='sstateProc', start=0*O, l=1*O,  typ='uint', verbose='SubState for Data Processing', disp='sstateProc',),
                                     CCSDSKey(name='sstatePldCom', start=1*O, l=1*O,  typ='uint', verbose='SubState for UART Payload Communication', disp='sstatePldCom',),
                                     CCSDSKey(name='sstateDataMgm', start=2*O, l=1*O,  typ='uint', verbose='SubState for Data Management', disp='sstateDataMgm',),
                                     CCSDSKey(name='sstateSdCard', start=3*O, l=1*O,  typ='uint', verbose='SubState for SD Card use', disp='sstateSdCard',)])
}


TROUSSEAU = CCSDSMetaTrousseau(TROUSSEAUDIC, key='telecommand_id_mirror')
