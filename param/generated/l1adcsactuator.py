#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1ADCSACTUATOR_KEYS = [
    dict(
        name = 'wheel_speed_x',
        start = 0*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Reaction Wheel Current Speed X',
        unit = 'rpm',
        disp = 'wheelSpeedX'),

    dict(
        name = 'wheel_target_x',
        start = 16*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelTargetX'),

    dict(
        name = 'wheel_mode_x',
        start = 32*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelModeX'),

    dict(
        name = 'wheel_speed_y',
        start = 40*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Reaction Wheel Current Speed Y',
        unit = 'rpm',
        disp = 'wheelSpeedY'),

    dict(
        name = 'wheel_target_y',
        start = 56*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelTargetY'),

    dict(
        name = 'wheel_mode_y',
        start = 72*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelModeY'),

    dict(
        name = 'wheel_speed_z',
        start = 80*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Reaction Wheel Current Speed Z',
        unit = 'rpm',
        disp = 'wheelSpeedZ'),

    dict(
        name = 'wheel_target_z',
        start = 96*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelTargetZ'),

    dict(
        name = 'wheel_mode_z',
        start = 112*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'wheelModeZ'),

    dict(
        name = 'magnetor_target_x',
        start = 120*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Magnetorquer Target X',
        unit = 'mA',
        disp = 'magnetorTargetX'),

    dict(
        name = 'magnetor_target_y',
        start = 136*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Magnetorquer Target Y',
        unit = 'mA',
        disp = 'magnetorTargetY'),

    dict(
        name = 'magnetor_target_z',
        start = 152*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Magnetorquer Target Z',
        unit = 'mA',
        disp = 'magnetorTargetZ'),

]

