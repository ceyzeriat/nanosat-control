#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1ADCSSENSOR_KEYS = [
    dict(
        name = 'mag_field_x',
        start = 0*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'magFieldX'),

    dict(
        name = 'mag_field_y',
        start = 32*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'magFieldY'),

    dict(
        name = 'mag_field_z',
        start = 64*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'magFieldZ'),

    dict(
        name = 'accelero_x',
        start = 96*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'AcceleroX'),

    dict(
        name = 'accelero_y',
        start = 128*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'AcceleroY'),

    dict(
        name = 'accelero_z',
        start = 160*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'AcceleroZ'),

    dict(
        name = 'gyro1_x',
        start = 192*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyro1X'),

    dict(
        name = 'gyro1_y',
        start = 224*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyro1Y'),

    dict(
        name = 'gyry1_z',
        start = 256*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyry1Z'),

    dict(
        name = 'gyro2_x',
        start = 288*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyro2X'),

    dict(
        name = 'gyro2_y',
        start = 320*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyro2Y'),

    dict(
        name = 'gyro2_z',
        start = 352*b,
        l = 32*b,
        typ = 'float',
        verbose = '[NO DOC STRING]',
        disp = 'Gyro2Z'),

    dict(
        name = 'st200_time',
        start = 384*b,
        l = 64*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'ST200Time'),

    dict(
        name = 'st200_time_ms',
        start = 448*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'ST200Time_ms'),

    dict(
        name = 'quaternion1',
        start = 464*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 1 from ADCS',
        disp = 'quaternion1'),

    dict(
        name = 'quaternion2',
        start = 496*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 2 from ADCS',
        disp = 'quaternion2'),

    dict(
        name = 'quaternion3',
        start = 528*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 3 from ADCS',
        disp = 'quaternion3'),

    dict(
        name = 'quaternion4',
        start = 560*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 4 from ADCS',
        disp = 'quaternion4'),

]

