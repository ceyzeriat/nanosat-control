#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1ADCSSTANDARD_KEYS = [
    dict(
        name = 'adcs_stat_flag_hl_op_tgt_cap',
        start = 12*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_CAP'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_fix_wgs84',
        start = 13*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_FIX_WGS84'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_nadir',
        start = 14*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_NADIR'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track',
        start = 15*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_const_v',
        start = 16*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_CONST_V'),

    dict(
        name = 'adcs_stat_flag_hl_op_spin',
        start = 17*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SPIN'),

    dict(
        name = 'adcs_stat_flag_hl_op_sunp',
        start = 19*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SUNP'),

    dict(
        name = 'adcs_stat_flag_hl_op_detumbling',
        start = 20*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_DETUMBLING'),

    dict(
        name = 'adcs_stat_flag_hl_op_measure',
        start = 21*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_MEASURE'),

    dict(
        name = 'adcs_stat_flag_datetime_valid',
        start = 27*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_DATETIME_VALID'),

    dict(
        name = 'adcs_stat_flag_hl_op_safe',
        start = 29*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SAFE'),

    dict(
        name = 'adcs_stat_flag_hl_op_idle',
        start = 30*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_IDLE'),

    dict(
        name = 'i_adcs_error',
        start = 32*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'iAdcsError'),

    dict(
        name = 'control_satus',
        start = 64*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'controlSatus'),

    dict(
        name = 'control_error',
        start = 96*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'controlError'),

    dict(
        name = 'livelyhood',
        start = 128*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'livelyhood'),

    dict(
        name = 'sec',
        start = 160*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Elapsed seconds since epoch',
        unit = 's',
        disp = 'sec'),

    dict(
        name = 'msec',
        start = 192*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Elapsed sub-seconds',
        unit = 'ms',
        disp = 'msec'),

    dict(
        name = 'gyro1',
        start = 208*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'Gyro 1 Temperature',
        unit = 'degC',
        disp = 'gyro1'),

    dict(
        name = 'gyro2',
        start = 216*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'Gyro 2 Temperature',
        unit = 'degC',
        disp = 'gyro2'),

    dict(
        name = 'mtq_x',
        start = 224*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'MTQ-X Temperature',
        unit = 'degC',
        disp = 'mtqX'),

    dict(
        name = 'mtq_y',
        start = 232*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'MTQ-Y Temperature',
        unit = 'degC',
        disp = 'mtqY'),

    dict(
        name = 'mtq_z',
        start = 240*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'MTQ-Z Temperature',
        unit = 'degC',
        disp = 'mtqZ'),

    dict(
        name = 'proc_temp',
        start = 248*b,
        l = 8*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'procTemp'),

    dict(
        name = 'rw_x_temp',
        start = 256*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'RW-X Temperature',
        unit = 'degC',
        disp = 'rwXTemp'),

    dict(
        name = 'rw_y_temp',
        start = 264*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'RW-Y Temperature',
        unit = 'degC',
        disp = 'rwYTemp'),

    dict(
        name = 'rw_z_temp',
        start = 272*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'RW-Z Temperature',
        unit = 'degC',
        disp = 'rwZTemp'),

    dict(
        name = 'st200_temp',
        start = 280*b,
        l = 8*b,
        typ = 'sint',
        verbose = 'ST200 Temperature',
        unit = 'degC',
        disp = 'st200Temp'),

    dict(
        name = 'mtq_current',
        start = 288*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'MTQ Current Consumption',
        unit = 'mA',
        disp = 'mtqCurrent'),

    dict(
        name = 'mtq_power',
        start = 304*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'MTQ Power Consumption',
        unit = 'mW',
        disp = 'mtqPower'),

    dict(
        name = 'mtq_supply',
        start = 320*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'MTQ Supply Voltage',
        unit = 'mV',
        disp = 'mtqSupply'),

    dict(
        name = 'st200_current',
        start = 336*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'ST200 Current Consumption',
        unit = 'mA',
        disp = 'st200Current'),

    dict(
        name = 'st200_power',
        start = 352*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'ST200 Power Consumption',
        unit = 'mW',
        disp = 'st200Power'),

    dict(
        name = 'st200_voltage',
        start = 368*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'ST200 Supply Voltage',
        unit = 'mV',
        disp = 'st200Voltage'),

    dict(
        name = 'iadcs_current',
        start = 384*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'iACDS 3.3V Current Consumption',
        unit = 'mA',
        disp = 'iadcsCurrent'),

    dict(
        name = 'iadcs_c_power',
        start = 400*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'iACDS 3.3V Power Consumption',
        unit = 'mW',
        disp = 'iadcsCPower'),

    dict(
        name = 'iadcs_voltage',
        start = 416*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'iACDS 3.3V Supply Voltage',
        unit = 'mV',
        disp = 'iadcsVoltage'),

    dict(
        name = 'rw_current',
        start = 432*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'RW Current Consumption',
        unit = 'mA',
        disp = 'rwCurrent'),

    dict(
        name = 'rw_power',
        start = 448*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'RW Power Consumption',
        unit = 'mW',
        disp = 'rwPower'),

    dict(
        name = 'rw_voltage',
        start = 464*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'RW Supply Voltage',
        unit = 'mV',
        disp = 'rwVoltage'),

]

