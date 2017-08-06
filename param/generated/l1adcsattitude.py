#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1ADCSATTITUDE_KEYS = [
    dict(
        name = 'quaternion1',
        start = 0*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 1 from ADCS',
        disp = 'quaternion1'),

    dict(
        name = 'quaternion2',
        start = 32*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 2 from ADCS',
        disp = 'quaternion2'),

    dict(
        name = 'quaternion3',
        start = 64*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 3 from ADCS',
        disp = 'quaternion3'),

    dict(
        name = 'quaternion4',
        start = 96*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 4 from ADCS',
        disp = 'quaternion4'),

    dict(
        name = 'angular_rate_x',
        start = 128*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateX'),

    dict(
        name = 'angular_rate_y',
        start = 160*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateY'),

    dict(
        name = 'angular_rate_z',
        start = 192*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateZ'),

]

