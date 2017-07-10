#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L0HKSTRUCTPART2_KEYS = [
dict(
         name = 'adcs_state',
         start = 0*b,
         l = 2*b,
         typ='uint',
         verbose = 'ADCS state',
         disp = 'adcsState'),

dict(
         name = 'solar_panel5_error_flag',
         start = 19*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel5ErrorFlag'),

dict(
         name = 'solar_panel4_error_flag',
         start = 20*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel4ErrorFlag'),

dict(
         name = 'solar_panel3_error_flag',
         start = 21*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel3ErrorFlag'),

dict(
         name = 'solar_panel2_error_flag',
         start = 22*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel2ErrorFlag'),

dict(
         name = 'solar_panel1_error_flag',
         start = 23*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel1ErrorFlag'),

dict(
         name = 'solar_panel_temp5',
         start = 24*b,
         l = 16*b,
         typ='uint',
         verbose = 'Temperature of solar panel 5',
         disp = 'solarPanelTemp5'),

dict(
         name = 'solar_panel_temp4',
         start = 40*b,
         l = 16*b,
         typ='uint',
         verbose = 'Temperature of solar panel 4',
         disp = 'solarPanelTemp4'),

dict(
         name = 'solar_panel_temp3',
         start = 56*b,
         l = 16*b,
         typ='uint',
         verbose = 'Temperature of solar panel 3',
         disp = 'solarPanelTemp3'),

dict(
         name = 'solar_panel_temp2',
         start = 72*b,
         l = 16*b,
         typ='uint',
         verbose = 'Temperature of solar panel 2',
         disp = 'solarPanelTemp2'),

dict(
         name = 'solar_panel_temp1',
         start = 88*b,
         l = 16*b,
         typ='uint',
         verbose = 'Temperature of solar panel 1',
         disp = 'solarPanelTemp1'),

]
