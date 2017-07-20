#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


def unram_solar_panel_temp5_zp(x, **kwargs):
    """
    verbose = x/64
    """
    return x/64

def unram_solar_panel_temp4_ym(x, **kwargs):
    """
    verbose = x/64
    """
    return x/64

def unram_solar_panel_temp3_yp(x, **kwargs):
    """
    verbose = x/64
    """
    return x/64

def unram_solar_panel_temp2_xm(x, **kwargs):
    """
    verbose = x/64
    """
    return x/64

def unram_solar_panel_temp1_xp(x, **kwargs):
    """
    verbose = x/64
    """
    return x/64

L0HKSTRUCTPART2_KEYS = [
    dict(
        name = 'solar_panel5_error_flag',
        start = 1*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'solarPanel5ErrorFlag'),

    dict(
        name = 'solar_panel4_error_flag',
        start = 2*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'solarPanel4ErrorFlag'),

    dict(
        name = 'solar_panel3_error_flag',
        start = 3*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'solarPanel3ErrorFlag'),

    dict(
        name = 'solar_panel2_error_flag',
        start = 4*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'solarPanel2ErrorFlag'),

    dict(
        name = 'solar_panel1_error_flag',
        start = 5*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'solarPanel1ErrorFlag'),

    dict(
        name = 'i_adcs_get_attitude_error',
        start = 6*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'iAdcsGetAttitudeError'),

    dict(
        name = 'i_adcs_get_status_register_error',
        start = 7*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'iAdcsGetStatusRegisterError'),

    dict(
        name = 'quaternion1',
        start = 8*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 1 from ADCS',
        disp = 'quaternion1'),

    dict(
        name = 'quaternion2',
        start = 40*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 2 from ADCS',
        disp = 'quaternion2'),

    dict(
        name = 'quaternion3',
        start = 72*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 3 from ADCS',
        disp = 'quaternion3'),

    dict(
        name = 'quaternion4',
        start = 104*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 4 from ADCS',
        disp = 'quaternion4'),

    dict(
        name = 'angular_rate_x',
        start = 136*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateX'),

    dict(
        name = 'angular_rate_y',
        start = 168*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateY'),

    dict(
        name = 'angular_rate_z',
        start = 200*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateZ'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_cap',
        start = 244*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_CAP'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_fix_wgs84',
        start = 245*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_FIX_WGS84'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_nadir',
        start = 246*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_NADIR'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track',
        start = 247*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_const_v',
        start = 248*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_CONST_V'),

    dict(
        name = 'adcs_stat_flag_hl_op_spin',
        start = 249*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SPIN'),

    dict(
        name = 'adcs_stat_flag_hl_op_sunp',
        start = 251*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SUNP'),

    dict(
        name = 'adcs_stat_flag_hl_op_detumbling',
        start = 252*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_DETUMBLING'),

    dict(
        name = 'adcs_stat_flag_hl_op_measure',
        start = 253*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_MEASURE'),

    dict(
        name = 'adcs_stat_flag_datetime_valid',
        start = 259*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_DATETIME_VALID'),

    dict(
        name = 'adcs_stat_flag_hl_op_safe',
        start = 261*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SAFE'),

    dict(
        name = 'adcs_stat_flag_hl_op_idle',
        start = 262*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_IDLE'),

    dict(
        name = 'solar_panel_temp5_zp',
        start = 264*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of solar panel 5 (Z)',
        unit = 'degC',
        fctunram = unram_solar_panel_temp5_zp,
        disp = 'solarPanelTemp5Zp'),

    dict(
        name = 'solar_panel_temp4_ym',
        start = 280*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of solar panel 4 (Y-)',
        unit = 'degC',
        fctunram = unram_solar_panel_temp4_ym,
        disp = 'solarPanelTemp4Ym'),

    dict(
        name = 'solar_panel_temp3_yp',
        start = 296*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of solar panel 3 (Y+)',
        unit = 'degC',
        fctunram = unram_solar_panel_temp3_yp,
        disp = 'solarPanelTemp3Yp'),

    dict(
        name = 'solar_panel_temp2_xm',
        start = 312*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of solar panel 2 (X-)',
        unit = 'degC',
        fctunram = unram_solar_panel_temp2_xm,
        disp = 'solarPanelTemp2Xm'),

    dict(
        name = 'solar_panel_temp1_xp',
        start = 328*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of solar panel 1 (X+)',
        unit = 'degC',
        fctunram = unram_solar_panel_temp1_xp,
        disp = 'solarPanelTemp1Xp'),

]

