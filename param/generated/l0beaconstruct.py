#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L0BEACONSTRUCT_KEYS = [
dict(
         name = 'solar_panel5_error_flag',
         start = 3*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel5ErrorFlag'),

dict(
         name = 'solar_panel4_error_flag',
         start = 4*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel4ErrorFlag'),

dict(
         name = 'solar_panel3_error_flag',
         start = 5*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel3ErrorFlag'),

dict(
         name = 'solar_panel2_error_flag',
         start = 6*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel2ErrorFlag'),

dict(
         name = 'solar_panel1_error_flag',
         start = 7*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'solarPanel1ErrorFlag'),

dict(
         name = 'fram_enable_error_flag',
         start = 9*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'framEnableErrorFlag'),

dict(
         name = 'ants_b_error_flag',
         start = 10*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsBErrorFlag'),

dict(
         name = 'ants_a_error_flag',
         start = 11*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsAErrorFlag'),

dict(
         name = 'trxvu_tx_error_flag',
         start = 12*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'trxvuTxErrorFlag'),

dict(
         name = 'trxvu_rx_error_flag',
         start = 13*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'trxvuRxErrorFlag'),

dict(
         name = 'obc_supervisor_error_flag',
         start = 14*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'obcSupervisorErrorFlag'),

dict(
         name = 'gom_eps_error_flag',
         start = 15*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'gomEpsErrorFlag'),

dict(
         name = 'ant1_undeployed_ants_b_status',
         start = 16*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1UndeployedAntsBStatus'),

dict(
         name = 'ant1_timeout_ants_b_status',
         start = 17*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1TimeoutAntsBStatus'),

dict(
         name = 'ant1_deploying_ants_b_status',
         start = 18*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1DeployingAntsBStatus'),

dict(
         name = 'ant2_undeployed_ants_b_status',
         start = 20*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2UndeployedAntsBStatus'),

dict(
         name = 'ant2_timeout_ants_b_status',
         start = 21*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2TimeoutAntsBStatus'),

dict(
         name = 'ant2_deploying_ants_b_status',
         start = 22*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2DeployingAntsBStatus'),

dict(
         name = 'ignore_flag_ants_b_status',
         start = 23*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ignoreFlagAntsBStatus'),

dict(
         name = 'ant3_undeployed_ants_b_status',
         start = 24*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3UndeployedAntsBStatus'),

dict(
         name = 'ant3_timeout_ants_b_status',
         start = 25*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3TimeoutAntsBStatus'),

dict(
         name = 'ant3_deploying_ants_b_status',
         start = 26*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3DeployingAntsBStatus'),

dict(
         name = 'ant4_undeployed_ants_b_status',
         start = 28*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4UndeployedAntsBStatus'),

dict(
         name = 'ant4_timeout_ants_b_status',
         start = 29*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4TimeoutAntsBStatus'),

dict(
         name = 'ant4_deploying_ants_b_status',
         start = 30*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4DeployingAntsBStatus'),

dict(
         name = 'armed_ants_b_status',
         start = 31*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'armedAntsBStatus'),

dict(
         name = 'ant1_undeployed_ants_a_status',
         start = 32*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1UndeployedAntsAStatus'),

dict(
         name = 'ant1_timeout_ants_a_status',
         start = 33*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1TimeoutAntsAStatus'),

dict(
         name = 'ant1_deploying_ants_a_status',
         start = 34*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1DeployingAntsAStatus'),

dict(
         name = 'ant2_undeployed_ants_a_status',
         start = 36*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2UndeployedAntsAStatus'),

dict(
         name = 'ant2_timeout_ants_a_status',
         start = 37*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2TimeoutAntsAStatus'),

dict(
         name = 'ant2_deploying_ants_a_status',
         start = 38*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2DeployingAntsAStatus'),

dict(
         name = 'ignore_flag_ants_a_status',
         start = 39*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ignoreFlagAntsAStatus'),

dict(
         name = 'ant3_undeployed_ants_a_status',
         start = 40*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3UndeployedAntsAStatus'),

dict(
         name = 'ant3_timeout_ants_a_status',
         start = 41*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3TimeoutAntsAStatus'),

dict(
         name = 'ant3_deploying_ants_a_status',
         start = 42*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3DeployingAntsAStatus'),

dict(
         name = 'ant4_undeployed_ants_a_status',
         start = 44*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4UndeployedAntsAStatus'),

dict(
         name = 'ant4_timeout_ants_a_status',
         start = 45*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4TimeoutAntsAStatus'),

dict(
         name = 'ant4_deploying_ants_a_status',
         start = 46*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4DeployingAntsAStatus'),

dict(
         name = 'armed_ants_a_status',
         start = 47*b,
         l = 1*b,
         typ='uint',
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'armedAntsAStatus'),

dict(
         name = 'solar_panel_temp5',
         start = 48*b,
         l = 2*O,
         typ='sint',
         verbose = 'Temperature of solar panel 5',
         disp = 'solarPanelTemp5'),

dict(
         name = 'solar_panel_temp4',
         start = 64*b,
         l = 2*O,
         typ='sint',
         verbose = 'Temperature of solar panel 4',
         disp = 'solarPanelTemp4'),

dict(
         name = 'solar_panel_temp3',
         start = 80*b,
         l = 2*O,
         typ='sint',
         verbose = 'Temperature of solar panel 3',
         disp = 'solarPanelTemp3'),

dict(
         name = 'solar_panel_temp2',
         start = 96*b,
         l = 2*O,
         typ='sint',
         verbose = 'Temperature of solar panel 2',
         disp = 'solarPanelTemp2'),

dict(
         name = 'solar_panel_temp1',
         start = 112*b,
         l = 2*O,
         typ='sint',
         verbose = 'Temperature of solar panel 1',
         disp = 'solarPanelTemp1'),

dict(
         name = 'ants_b_temp',
         start = 128*b,
         l = 2*O,
         typ='uint',
         verbose = 'Antenna system B temperature',
         disp = 'antsBTemp'),

dict(
         name = 'ants_a_temp',
         start = 144*b,
         l = 2*O,
         typ='uint',
         verbose = 'Antenna system A temperature',
         disp = 'antsATemp'),

dict(
         name = 'trxvu_tx_pa_temp',
         start = 160*b,
         l = 2*O,
         typ='uint',
         verbose = 'Trxvu tx power amplifier temp from l0HkStructPart1.txTrxvuHK.pa_temp',
         disp = 'TrxvuTxPaTemp'),

dict(
         name = 'trxvu_rx_pa_temp',
         start = 176*b,
         l = 2*O,
         typ='uint',
         verbose = 'Trxvu rx power amplifier temp from l0HkStructPart1.rxTrxvuHK.pa_temp',
         disp = 'TrxvuRxPaTemp'),

dict(
         name = 'trxvu_rx_board_temp',
         start = 192*b,
         l = 2*O,
         typ='uint',
         verbose = 'Trxvu rxBoard temp from l0HkStructPart1.rxTrxvuHK.board_temp',
         disp = 'TrxvuRxBoardTemp'),

dict(
         name = 'temp_bat2',
         start = 208*b,
         l = 2*O,
         typ='sint',
         verbose = 'Battery temperature 2 from l0HkStructPart1.epsHK.temp5',
         disp = 'tempBat2'),

dict(
         name = 'temp_bat1',
         start = 224*b,
         l = 2*O,
         typ='sint',
         verbose = 'Battery temperature 1 from l0HkStructPart1.epsHK.temp4',
         disp = 'tempBat1'),

dict(
         name = 'bat_mode',
         start = 240*b,
         l = 1*O,
         typ='uint',
         verbose = 'Battery mode [0 = normal, 1 = undervoltage, 2 = overvoltage] from l0HkStructPart1.epsHK.battmode',
         disp = 'batMode'),

dict(
         name = 'v_bat',
         start = 248*b,
         l = 2*O,
         typ='uint',
         verbose = 'Battery charge level (mV) from l0HkStructPart1.epsHK.vbatt',
         disp = 'vBat'),

dict(
         name = 'reboot_cause_eps',
         start = 264*b,
         l = 4*O,
         typ='uint',
         verbose = 'Reboot cause (from EPS) from l0HkStructPart1.epsHK.bootcause',
         disp = 'rebootCauseEps'),

dict(
         name = 'n_reboots_eps',
         start = 296*b,
         l = 4*O,
         typ='uint',
         verbose = 'Number of EPS reboots from l0HkStructPart1.epsHK.counter_boot',
         disp = 'nRebootsEps'),

dict(
         name = 'n_reboots_obc',
         start = 328*b,
         l = 4*O,
         typ='uint',
         verbose = 'Number of OBC reboots',
         disp = 'nRebootsObc'),

dict(
         name = 'up_time',
         start = 360*b,
         l = 4*O,
         typ='uint',
         verbose = 'OBC uptime in seconds',
         disp = 'upTime'),

dict(
         name = 'last_fram_log_fun_err_code',
         start = 392*b,
         l = 2*O,
         typ='sint',
         verbose = 'FunErrCode field of the last entry in the FRAM log',
         disp = 'lastFramLogFunErrCode'),

dict(
         name = 'last_fram_log_counter',
         start = 408*b,
         l = 2*O,
         typ='uint',
         verbose = 'Counter field of the last entry in the FRAM log',
         disp = 'lastFramLogCounter'),

dict(
         name = 'average_photon_count',
         start = 424*b,
         l = 2*O,
         typ='uint',
         verbose = 'Photon count from the payload, filled by L1',
         disp = 'averagePhotonCount'),

dict(
         name = 'sat_mode',
         start = 440*b,
         l = 1*O,
         typ='uint',
         verbose = 'Mode: L0 = 0, L1 = state machine mode ID',
         disp = 'satMode'),

dict(
         name = 'tc_sequence_count',
         start = 448*b,
         l = 2*O,
         typ='uint',
         verbose = 'Current OBC sequence count',
         disp = 'tcsqcnt'),

]
