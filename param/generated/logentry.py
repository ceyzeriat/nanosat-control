#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


LOGENTRY_KEYS = [
    dict(
        name = 'data',
        start = 0*b,
        l = 32*b,
        typ = 'hex',
        verbose = 'Optional error data',
        disp = 'data'),

    dict(
        name = 'ms_count',
        start = 32*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time tag field 2: number of milliseconds since start of day',
        unit = 'ms',
        disp = 'msCount'),

    dict(
        name = 'date',
        start = 48*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Time tag field 1: number of days since reference',
        unit = 'days',
        disp = 'date'),

    dict(
        name = 'fun_err_code',
        start = 80*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'funErrCode'),

    dict(
        name = 'line_code',
        start = 96*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'lineCode'),

    dict(
        name = 'file_crc_code',
        start = 112*b,
        l = 32*b,
        typ = 'hex',
        verbose = 'Identifies the file where the event was thrown',
        disp = 'fileCrcCode'),

    dict(
        name = 'log_counter',
        start = 144*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'logCounter'),

]

