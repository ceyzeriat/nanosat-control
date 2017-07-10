#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


BOOTERRORSTRUCT_KEYS = [
dict(
         name = 'adcs_power_on',
         start = 0*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'adcsPowerOn'),

dict(
         name = 'init_sd_card_system',
         start = 2*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'initSDCardSystem'),

dict(
         name = 'isis_solar_panelv2_initialize',
         start = 4*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'IsisSolarPanelv2_initialize'),

dict(
         name = 'gom_eps_initialize',
         start = 6*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'GomEpsInitialize'),

dict(
         name = 'supervisor_start',
         start = 8*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'Supervisor_start'),

dict(
         name = 'spi_start_bus1',
         start = 10*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'SPI_start_bus1'),

dict(
         name = 'spi_start_bus0',
         start = 12*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'SPI_start_bus0'),

dict(
         name = 'init_fram_log',
         start = 14*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'initFramLog'),

dict(
         name = 'time_start',
         start = 16*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'Time_start'),

dict(
         name = 'rtc_start',
         start = 18*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'RTC_start'),

dict(
         name = 'init_all_flags',
         start = 20*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'initAllFlags'),

dict(
         name = 'fram_start',
         start = 22*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'FRAM_start'),

dict(
         name = 'isis_ant_s_initialize',
         start = 24*O,
         l = 2*O,
         typ='sint',
         verbose = '[NO DOC STRING]',
         disp = 'IsisAntS_initialize'),

]