#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1DATACOVAR_KEYS = [
    dict(
        name = 'steps_i',
        start = 0*b,
        l = 8*b,
        typ = 'uint',
        verbose = 'Covariance i',
        disp = 'coVariance_j'),

    dict(
        name = 'steps_j',
        start = 8*b,
        l = 8*b,
        typ = 'uint',
        verbose = 'Covariance i',
        disp = 'coVariance_i'),

    dict(
        name = 'nsum',
        start = 16*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'Nsum'),

    dict(
        name = 'count_co_var',
        start = 24*b,
        l = 64*b,
        typ = 'uint',
        verbose = 'Covariance between i and j position',
        unit = 'ADU2',
        disp = 'coVariance'),

]

