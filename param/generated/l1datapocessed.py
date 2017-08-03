#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1DATAPOCESSED_KEYS = [
    dict(
        name = 'steps',
        start = 0*b,
        l = 8*b,
        typ = 'uint',
        verbose = 'steps position in the pattern cylce',
        disp = 'i'),

    dict(
        name = 'nsum',
        start = 8*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'Nsum'),

    dict(
        name = 'counts',
        start = 16*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        unit = 'ADU',
        disp = 'counts'),

    dict(
        name = 'xcom',
        start = 48*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'X piezo command in Volts',
        unit = 'Volts',
        disp = 'commandePiezoX'),

    dict(
        name = 'ycom',
        start = 80*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Y piezo command in Volts',
        unit = 'Volts',
        disp = 'commandePiezoY'),

    dict(
        name = 'xpos',
        start = 112*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'X position measured by sensor jauge',
        unit = 'um',
        disp = 'positionPiezoX'),

    dict(
        name = 'ypos',
        start = 144*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Y position measured by sensor jauge',
        unit = 'um',
        disp = 'positionPiezoY'),

    dict(
        name = 'counts_var',
        start = 176*b,
        l = 64*b,
        typ = 'uint',
        verbose = 'sum over Nsum of counts^2',
        unit = 'ADU2',
        disp = 'variance'),

    dict(
        name = 'xpos_var',
        start = 240*b,
        l = 64*b,
        typ = 'uint',
        verbose = 'sum over Nsum of xpos^2',
        unit = 'um2',
        disp = 'variance'),

    dict(
        name = 'ypos_var',
        start = 304*b,
        l = 64*b,
        typ = 'uint',
        verbose = 'sum over Nsum of ypos^2',
        unit = 'um2',
        disp = 'variance'),

]

