#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


def unram_solar_panel_temp5(x, **kwargs):
    """
    verbose = 16*x
    """
    return 16*x

def unram_solar_panel_temp4(x, **kwargs):
    """
    verbose = 16*x
    """
    return 16*x

def unram_solar_panel_temp3(x, **kwargs):
    """
    verbose = 16*x
    """
    return 16*x

def unram_solar_panel_temp2(x, **kwargs):
    """
    verbose = 16*x
    """
    return 16*x

def unram_solar_panel_temp1(x, **kwargs):
    """
    verbose = 16*x
    """
    return 16*x

def unram_ants_b_temp(x, **kwargs):
    """
    verbose = -0.2922*x+190.65
    """
    return -0.2922*x+190.65

def unram_ants_a_temp(x, **kwargs):
    """
    verbose = -0.2922*x+190.65
    """
    return -0.2922*x+190.65

def unram_trxvu_tx_pa_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

def unram_trxvu_rx_pa_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

def unram_trxvu_rx_board_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

L0BEACONSTRUCT_KEYS = [
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
        name = 'fram_enable_error_flag',
        start = 9*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'framEnableErrorFlag'),

    dict(
        name = 'ants_b_error_flag',
        start = 10*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'antsBErrorFlag'),

    dict(
        name = 'ants_a_error_flag',
        start = 11*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'antsAErrorFlag'),

    dict(
        name = 'trxvu_tx_error_flag',
        start = 12*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'trxvuTxErrorFlag'),

    dict(
        name = 'trxvu_rx_error_flag',
        start = 13*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'trxvuRxErrorFlag'),

    dict(
        name = 'obc_supervisor_error_flag',
        start = 14*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcSupervisorErrorFlag'),

    dict(
        name = 'gom_eps_error_flag',
        start = 15*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'gomEpsErrorFlag'),

    dict(
        name = 'ant1_undeployed_ants_b_status',
        start = 16*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1UndeployedAntsBStatus'),

    dict(
        name = 'ant1_timeout_ants_b_status',
        start = 17*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1TimeoutAntsBStatus'),

    dict(
        name = 'ant1_deploying_ants_b_status',
        start = 18*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1DeployingAntsBStatus'),

    dict(
        name = 'ant2_undeployed_ants_b_status',
        start = 20*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2UndeployedAntsBStatus'),

    dict(
        name = 'ant2_timeout_ants_b_status',
        start = 21*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2TimeoutAntsBStatus'),

    dict(
        name = 'ant2_deploying_ants_b_status',
        start = 22*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2DeployingAntsBStatus'),

    dict(
        name = 'ignore_flag_ants_b_status',
        start = 23*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ignoreFlagAntsBStatus'),

    dict(
        name = 'ant3_undeployed_ants_b_status',
        start = 24*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3UndeployedAntsBStatus'),

    dict(
        name = 'ant3_timeout_ants_b_status',
        start = 25*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3TimeoutAntsBStatus'),

    dict(
        name = 'ant3_deploying_ants_b_status',
        start = 26*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3DeployingAntsBStatus'),

    dict(
        name = 'ant4_undeployed_ants_b_status',
        start = 28*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4UndeployedAntsBStatus'),

    dict(
        name = 'ant4_timeout_ants_b_status',
        start = 29*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4TimeoutAntsBStatus'),

    dict(
        name = 'ant4_deploying_ants_b_status',
        start = 30*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4DeployingAntsBStatus'),

    dict(
        name = 'armed_ants_b_status',
        start = 31*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'armedAntsBStatus'),

    dict(
        name = 'ant1_undeployed_ants_a_status',
        start = 32*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1UndeployedAntsAStatus'),

    dict(
        name = 'ant1_timeout_ants_a_status',
        start = 33*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1TimeoutAntsAStatus'),

    dict(
        name = 'ant1_deploying_ants_a_status',
        start = 34*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1DeployingAntsAStatus'),

    dict(
        name = 'ant2_undeployed_ants_a_status',
        start = 36*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2UndeployedAntsAStatus'),

    dict(
        name = 'ant2_timeout_ants_a_status',
        start = 37*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2TimeoutAntsAStatus'),

    dict(
        name = 'ant2_deploying_ants_a_status',
        start = 38*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2DeployingAntsAStatus'),

    dict(
        name = 'ignore_flag_ants_a_status',
        start = 39*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ignoreFlagAntsAStatus'),

    dict(
        name = 'ant3_undeployed_ants_a_status',
        start = 40*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3UndeployedAntsAStatus'),

    dict(
        name = 'ant3_timeout_ants_a_status',
        start = 41*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3TimeoutAntsAStatus'),

    dict(
        name = 'ant3_deploying_ants_a_status',
        start = 42*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3DeployingAntsAStatus'),

    dict(
        name = 'ant4_undeployed_ants_a_status',
        start = 44*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4UndeployedAntsAStatus'),

    dict(
        name = 'ant4_timeout_ants_a_status',
        start = 45*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4TimeoutAntsAStatus'),

    dict(
        name = 'ant4_deploying_ants_a_status',
        start = 46*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4DeployingAntsAStatus'),

    dict(
        name = 'armed_ants_a_status',
        start = 47*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'armedAntsAStatus'),

    dict(
        name = 'solar_panel_temp5',
        start = 48*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature of solar panel 5',
        unit = 'degC',
        fctunram = unram_solar_panel_temp5,
        disp = 'solarPanelTemp5'),

    dict(
        name = 'solar_panel_temp4',
        start = 64*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature of solar panel 4',
        unit = 'degC',
        fctunram = unram_solar_panel_temp4,
        disp = 'solarPanelTemp4'),

    dict(
        name = 'solar_panel_temp3',
        start = 80*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature of solar panel 3',
        unit = 'degC',
        fctunram = unram_solar_panel_temp3,
        disp = 'solarPanelTemp3'),

    dict(
        name = 'solar_panel_temp2',
        start = 96*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature of solar panel 2',
        unit = 'degC',
        fctunram = unram_solar_panel_temp2,
        disp = 'solarPanelTemp2'),

    dict(
        name = 'solar_panel_temp1',
        start = 112*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature of solar panel 1',
        unit = 'degC',
        fctunram = unram_solar_panel_temp1,
        disp = 'solarPanelTemp1'),

    dict(
        name = 'ants_b_temp',
        start = 128*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of antenna system (side B)',
        unit = 'degC',
        fctunram = unram_ants_b_temp,
        disp = 'antsBTemp'),

    dict(
        name = 'ants_a_temp',
        start = 144*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of antenna system (side A)',
        unit = 'degC',
        fctunram = unram_ants_a_temp,
        disp = 'antsATemp'),

    dict(
        name = 'trxvu_tx_pa_temp',
        start = 160*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Tx board power amplifier temperature',
        unit = 'degC',
        fctunram = unram_trxvu_tx_pa_temp,
        disp = 'TrxvuTxPaTemp'),

    dict(
        name = 'trxvu_rx_pa_temp',
        start = 176*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx power amplifier temperature',
        unit = 'degC',
        fctunram = unram_trxvu_rx_pa_temp,
        disp = 'TrxvuRxPaTemp'),

    dict(
        name = 'trxvu_rx_board_temp',
        start = 192*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board temperature',
        unit = 'degC',
        fctunram = unram_trxvu_rx_board_temp,
        disp = 'TrxvuRxBoardTemp'),

    dict(
        name = 'temp_bat2',
        start = 208*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Battery temperature 2',
        unit = 'degC',
        disp = 'tempBat2'),

    dict(
        name = 'temp_bat1',
        start = 224*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Battery temperature 1',
        unit = 'degC',
        disp = 'tempBat1'),

    dict(
        name = 'bat_mode',
        start = 240*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'batMode'),

    dict(
        name = 'v_bat',
        start = 248*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Battery charge voltage',
        unit = 'mV',
        disp = 'vBat'),

    dict(
        name = 'reboot_cause_eps',
        start = 264*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'rebootCauseEps'),

    dict(
        name = 'n_reboots_eps',
        start = 296*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'nRebootsEps'),

    dict(
        name = 'n_reboots_obc',
        start = 328*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'nRebootsObc'),

    dict(
        name = 'quaternion1',
        start = 360*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 1 from ADCS',
        disp = 'quaternion1'),

    dict(
        name = 'quaternion2',
        start = 392*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 2 from ADCS',
        disp = 'quaternion2'),

    dict(
        name = 'quaternion3',
        start = 424*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 3 from ADCS',
        disp = 'quaternion3'),

    dict(
        name = 'quaternion4',
        start = 456*b,
        l = 32*b,
        typ = 'float',
        verbose = 'attitude quaternion 4 from ADCS',
        disp = 'quaternion4'),

    dict(
        name = 'angular_rate_x',
        start = 488*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateX'),

    dict(
        name = 'angular_rate_y',
        start = 520*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateY'),

    dict(
        name = 'angular_rate_z',
        start = 552*b,
        l = 32*b,
        typ = 'float',
        verbose = 'angular rotation speed (X axis) from ADCS',
        unit = 'rad/s',
        disp = 'angularRateZ'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_cap',
        start = 596*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_CAP'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_fix_wgs84',
        start = 597*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_FIX_WGS84'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_nadir',
        start = 598*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_NADIR'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track',
        start = 599*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK'),

    dict(
        name = 'adcs_stat_flag_hl_op_tgt_track_const_v',
        start = 600*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_TGT_TRACK_CONST_V'),

    dict(
        name = 'adcs_stat_flag_hl_op_spin',
        start = 601*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SPIN'),

    dict(
        name = 'adcs_stat_flag_hl_op_sunp',
        start = 603*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SUNP'),

    dict(
        name = 'adcs_stat_flag_hl_op_detumbling',
        start = 604*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_DETUMBLING'),

    dict(
        name = 'adcs_stat_flag_hl_op_measure',
        start = 605*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_MEASURE'),

    dict(
        name = 'adcs_stat_flag_datetime_valid',
        start = 611*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_DATETIME_VALID'),

    dict(
        name = 'adcs_stat_flag_hl_op_safe',
        start = 613*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_SAFE'),

    dict(
        name = 'adcs_stat_flag_hl_op_idle',
        start = 614*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ADCS_STAT_FLAG_HL_OP_IDLE'),

    dict(
        name = 'up_time',
        start = 616*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'OBC uptime',
        unit = 's',
        disp = 'upTime'),

    dict(
        name = 'last_fram_log_fun_err_code',
        start = 648*b,
        l = 16*b,
        typ = 'sint',
        verbose = '[NO DOC STRING]',
        disp = 'lastFramLogFunErrCode'),

    dict(
        name = 'last_fram_log_line_code',
        start = 664*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'lastFramLogLineCode'),

    dict(
        name = 'last_fram_log_file_crc_code',
        start = 680*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'lastFramLogFileCrcCode'),

    dict(
        name = 'last_fram_log_counter',
        start = 712*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'lastFramLogCounter'),

    dict(
        name = 'average_photon_count',
        start = 728*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'averagePhotonCount'),

    dict(
        name = 'sat_mode',
        start = 744*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'satMode'),

    dict(
        name = 'tc_sequence_count',
        start = 752*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'tcSequenceCount'),

]

