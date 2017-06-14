
from ctrl.utils import bincore

L0HKSTRUCTPART2_KEYS = [
dict(
         name = 'adcs_state',
         start = 0,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADCS state',
         disp = 'adcsState'),

dict(
         name = 'solar_panel5_error_flag',
         start = 19,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel5ErrorFlag'),

dict(
         name = 'solar_panel4_error_flag',
         start = 20,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel4ErrorFlag'),

dict(
         name = 'solar_panel3_error_flag',
         start = 21,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel3ErrorFlag'),

dict(
         name = 'solar_panel2_error_flag',
         start = 22,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel2ErrorFlag'),

dict(
         name = 'solar_panel1_error_flag',
         start = 23,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel1ErrorFlag'),

dict(
         name = 'solar_panel_temp5',
         start = 24,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Temperature of solar panel 5',
         disp = 'solarPanelTemp5'),

dict(
         name = 'solar_panel_temp4',
         start = 40,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Temperature of solar panel 4',
         disp = 'solarPanelTemp4'),

dict(
         name = 'solar_panel_temp3',
         start = 56,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Temperature of solar panel 3',
         disp = 'solarPanelTemp3'),

dict(
         name = 'solar_panel_temp2',
         start = 72,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Temperature of solar panel 2',
         disp = 'solarPanelTemp2'),

dict(
         name = 'solar_panel_temp1',
         start = 88,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Temperature of solar panel 1',
         disp = 'solarPanelTemp1'),

]
