
from ctrl.utils import bincore

BOOTERRORSTRUCT_KEYS = [
dict(
         name = 'adcs_power_on',
         start = 0,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'adcsPowerOn'),

dict(
         name = 'init_sd_card_system',
         start = 16,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'initSDCardSystem'),

dict(
         name = 'isis_solar_panelv2_initialize',
         start = 32,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'IsisSolarPanelv2_initialize'),

dict(
         name = 'gom_eps_initialize',
         start = 48,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'GomEpsInitialize'),

dict(
         name = 'supervisor_start',
         start = 64,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'Supervisor_start'),

dict(
         name = 'spi_start_bus1',
         start = 80,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'SPI_start_bus1'),

dict(
         name = 'spi_start_bus0',
         start = 96,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'SPI_start_bus0'),

dict(
         name = 'init_fram_log',
         start = 112,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'initFramLog'),

dict(
         name = 'time_start',
         start = 128,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'Time_start'),

dict(
         name = 'rtc_start',
         start = 144,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'RTC_start'),

dict(
         name = 'init_all_flags',
         start = 160,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'initAllFlags'),

dict(
         name = 'fram_start',
         start = 176,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'FRAM_start'),

dict(
         name = 'isis_ant_s_initialize',
         start = 192,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = '[NO DOC STRING]',
         disp = 'IsisAntS_initialize'),

]