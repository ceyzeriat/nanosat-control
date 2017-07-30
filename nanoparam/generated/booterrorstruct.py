#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nanoctrl.utils import bincore
from nanoctrl.utils import b
from nanoctrl.utils import O


BOOTERRORSTRUCT_KEYS = [
    dict(
        name = 'adcs_power_on',
        start = 0*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'adcsPowerOn'),

    dict(
        name = 'init_sd_card_system',
        start = 16*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'initSDCardSystem'),

    dict(
        name = 'isis_solar_panelv2_initialize',
        start = 32*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'IsisSolarPanelv2_initialize'),

    dict(
        name = 'gom_eps_initialize',
        start = 48*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'GomEpsInitialize'),

    dict(
        name = 'supervisor_start',
        start = 64*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'Supervisor_start'),

    dict(
        name = 'spi_start_bus1',
        start = 80*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'SPI_start_bus1'),

    dict(
        name = 'spi_start_bus0',
        start = 96*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'SPI_start_bus0'),

    dict(
        name = 'init_fram_log',
        start = 112*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'initFramLog'),

    dict(
        name = 'time_start',
        start = 128*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'Time_start'),

    dict(
        name = 'rtc_start',
        start = 144*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'RTC_start'),

    dict(
        name = 'init_all_flags',
        start = 160*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'initAllFlags'),

    dict(
        name = 'fram_start',
        start = 176*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'FRAM_start'),

    dict(
        name = 'isis_ant_s_initialize',
        start = 192*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'IsisAntS_initialize'),

    dict(
        name = 'i2_c_start',
        start = 208*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'I2C_start'),

]

