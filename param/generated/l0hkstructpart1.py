#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


def unram_ants_temperature_side_b(x, **kwargs):
    """
    verbose = -0.2922*x+190.65
    """
    return -0.2922*x+190.65

def unram_ants_temperature_side_a(x, **kwargs):
    """
    verbose = -0.2922*x+190.65
    """
    return -0.2922*x+190.65

def unram_tx_trxvu_hk_current(x, **kwargs):
    """
    verbose = 0.16643964*x#??
    """
    return 0.16643964*x#??

def unram_tx_trxvu_hk_forwardpower(x, **kwargs):
    """
    verbose = 0.00005887*x*x#??
    """
    return 0.00005887*x*x#??

def unram_tx_trxvu_hk_pa_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

def unram_tx_trxvu_hk_tx_reflectedpower(x, **kwargs):
    """
    verbose = 0.00005887*x*x#??
    """
    return 0.00005887*x*x#??

def unram_rx_trxvu_hk_rssi(x, **kwargs):
    """
    verbose = 0.03*x-152#??
    """
    return 0.03*x-152#??

def unram_rx_trxvu_hk_pa_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

def unram_rx_trxvu_hk_board_temp(x, **kwargs):
    """
    verbose = -0.07669*x+195.6037#??
    """
    return -0.07669*x+195.6037#??

def unram_rx_trxvu_hk_bus_volt(x, **kwargs):
    """
    verbose = 0.00488*x#??
    """
    return 0.00488*x#??

def unram_rx_trxvu_hk_rx_current(x, **kwargs):
    """
    verbose = 0.16643964*x#??
    """
    return 0.16643964*x#??

def unram_rx_trxvu_hk_rx_doppler(x, **kwargs):
    """
    verbose = 13.352*x-22300#??
    """
    return 13.352*x-22300#??

def unram_rx_trxvu_hk_tx_current(x, **kwargs):
    """
    verbose = 0#??
    """
    return 0#??

L0HKSTRUCTPART1_KEYS = [
    dict(
        name = 'fram_enable_error_flag',
        start = 1*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'framEnableErrorFlag'),

    dict(
        name = 'ants_b_error_flag',
        start = 2*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'antsBErrorFlag'),

    dict(
        name = 'ants_a_error_flag',
        start = 3*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'antsAErrorFlag'),

    dict(
        name = 'trxvu_tx_error_flag',
        start = 4*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'trxvuTxErrorFlag'),

    dict(
        name = 'trxvu_rx_error_flag',
        start = 5*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'trxvuRxErrorFlag'),

    dict(
        name = 'obc_supervisor_error_flag',
        start = 6*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcSupervisorErrorFlag'),

    dict(
        name = 'gom_eps_error_flag',
        start = 7*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'gomEpsErrorFlag'),

    dict(
        name = 'ants_uptime_b',
        start = 8*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Uptime of antenna system (side B)',
        unit = 's',
        disp = 'antsUptimeB'),

    dict(
        name = 'ant1_undeployed_ants_b_status',
        start = 40*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1UndeployedAntsBStatus'),

    dict(
        name = 'ant1_timeout_ants_b_status',
        start = 41*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1TimeoutAntsBStatus'),

    dict(
        name = 'ant1_deploying_ants_b_status',
        start = 42*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1DeployingAntsBStatus'),

    dict(
        name = 'ant2_undeployed_ants_b_status',
        start = 44*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2UndeployedAntsBStatus'),

    dict(
        name = 'ant2_timeout_ants_b_status',
        start = 45*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2TimeoutAntsBStatus'),

    dict(
        name = 'ant2_deploying_ants_b_status',
        start = 46*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2DeployingAntsBStatus'),

    dict(
        name = 'ignore_flag_ants_b_status',
        start = 47*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ignoreFlagAntsBStatus'),

    dict(
        name = 'ant3_undeployed_ants_b_status',
        start = 48*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3UndeployedAntsBStatus'),

    dict(
        name = 'ant3_timeout_ants_b_status',
        start = 49*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3TimeoutAntsBStatus'),

    dict(
        name = 'ant3_deploying_ants_b_status',
        start = 50*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3DeployingAntsBStatus'),

    dict(
        name = 'ant4_undeployed_ants_b_status',
        start = 52*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4UndeployedAntsBStatus'),

    dict(
        name = 'ant4_timeout_ants_b_status',
        start = 53*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4TimeoutAntsBStatus'),

    dict(
        name = 'ant4_deploying_ants_b_status',
        start = 54*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4DeployingAntsBStatus'),

    dict(
        name = 'armed_ants_b_status',
        start = 55*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'armedAntsBStatus'),

    dict(
        name = 'ants_temperature_side_b',
        start = 56*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of antenna system (side B)',
        unit = 'degC',
        fctunram = unram_ants_temperature_side_b,
        disp = 'antsTemperatureSideB'),

    dict(
        name = 'ants_uptime_a',
        start = 72*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Uptime of antenna system (side A)',
        unit = 's',
        disp = 'antsUptimeA'),

    dict(
        name = 'ant1_undeployed_ants_a_status',
        start = 104*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1UndeployedAntsAStatus'),

    dict(
        name = 'ant1_timeout_ants_a_status',
        start = 105*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1TimeoutAntsAStatus'),

    dict(
        name = 'ant1_deploying_ants_a_status',
        start = 106*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant1DeployingAntsAStatus'),

    dict(
        name = 'ant2_undeployed_ants_a_status',
        start = 108*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2UndeployedAntsAStatus'),

    dict(
        name = 'ant2_timeout_ants_a_status',
        start = 109*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2TimeoutAntsAStatus'),

    dict(
        name = 'ant2_deploying_ants_a_status',
        start = 110*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant2DeployingAntsAStatus'),

    dict(
        name = 'ignore_flag_ants_a_status',
        start = 111*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ignoreFlagAntsAStatus'),

    dict(
        name = 'ant3_undeployed_ants_a_status',
        start = 112*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3UndeployedAntsAStatus'),

    dict(
        name = 'ant3_timeout_ants_a_status',
        start = 113*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3TimeoutAntsAStatus'),

    dict(
        name = 'ant3_deploying_ants_a_status',
        start = 114*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant3DeployingAntsAStatus'),

    dict(
        name = 'ant4_undeployed_ants_a_status',
        start = 116*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4UndeployedAntsAStatus'),

    dict(
        name = 'ant4_timeout_ants_a_status',
        start = 117*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4TimeoutAntsAStatus'),

    dict(
        name = 'ant4_deploying_ants_a_status',
        start = 118*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'ant4DeployingAntsAStatus'),

    dict(
        name = 'armed_ants_a_status',
        start = 119*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'armedAntsAStatus'),

    dict(
        name = 'ants_temperature_side_a',
        start = 120*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature of antenna system (side A)',
        unit = 'degC',
        fctunram = unram_ants_temperature_side_a,
        disp = 'antsTemperatureSideA'),

    dict(
        name = 'tx_trxvu_hk_current',
        start = 136*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Tx board transmitter current',
        unit = 'mA',
        fctunram = unram_tx_trxvu_hk_current,
        disp = 'txTrxvuHkCurrent'),

    dict(
        name = 'tx_trxvu_hk_forwardpower',
        start = 152*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Tx board forward power',
        unit = 'mW',
        fctunram = unram_tx_trxvu_hk_forwardpower,
        disp = 'txTrxvuHkForwardpower'),

    dict(
        name = 'tx_trxvu_hk_pa_temp',
        start = 168*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Tx board power amplifier temperature',
        unit = 'degC',
        fctunram = unram_tx_trxvu_hk_pa_temp,
        disp = 'txTrxvuHkPaTemp'),

    dict(
        name = 'tx_trxvu_hk_tx_reflectedpower',
        start = 184*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Tx board reflected power',
        unit = 'mW',
        fctunram = unram_tx_trxvu_hk_tx_reflectedpower,
        disp = 'txTrxvuHkTxReflectedpower'),

    dict(
        name = 'rx_trxvu_hk_rssi',
        start = 200*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx rssi measurement',
        unit = 'dBm',
        fctunram = unram_rx_trxvu_hk_rssi,
        disp = 'rxTrxvuHkRssi'),

    dict(
        name = 'rx_trxvu_hk_pa_temp',
        start = 216*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx power amplifier temperature',
        unit = 'degC',
        fctunram = unram_rx_trxvu_hk_pa_temp,
        disp = 'rxTrxvuHkPaTemp'),

    dict(
        name = 'rx_trxvu_hk_board_temp',
        start = 232*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board temperature',
        unit = 'degC',
        fctunram = unram_rx_trxvu_hk_board_temp,
        disp = 'rxTrxvuHkBoardTemp'),

    dict(
        name = 'rx_trxvu_hk_bus_volt',
        start = 248*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board bus voltage',
        unit = 'mV',
        fctunram = unram_rx_trxvu_hk_bus_volt,
        disp = 'rxTrxvuHkBusVolt'),

    dict(
        name = 'rx_trxvu_hk_rx_current',
        start = 264*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board receiver current',
        unit = 'mA',
        fctunram = unram_rx_trxvu_hk_rx_current,
        disp = 'rxTrxvuHkRxCurrent'),

    dict(
        name = 'rx_trxvu_hk_rx_doppler',
        start = 280*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board receiver doppler',
        unit = 'Hz',
        fctunram = unram_rx_trxvu_hk_rx_doppler,
        disp = 'rxTrxvuHkRxDoppler'),

    dict(
        name = 'rx_trxvu_hk_tx_current',
        start = 296*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu Rx board transmitter current',
        unit = 'mA',
        fctunram = unram_rx_trxvu_hk_tx_current,
        disp = 'rxTrxvuHkTxCurrent'),

    dict(
        name = 'obc_hk_crc8',
        start = 312*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkCrc8'),

    dict(
        name = 'obc_hk_adc_update_flag',
        start = 320*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkAdcUpdateFlag'),

    dict(
        name = 'obc_hk_rtc_voltage',
        start = 328*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage RTC (ADC 10)',
        unit = 'mV',
        disp = 'obcHkRtcVoltage'),

    dict(
        name = 'obc_hk1p0_current',
        start = 344*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current 1.0V (ADC 9)',
        unit = 'mA',
        disp = 'obcHk1p0Current'),

    dict(
        name = 'obc_hk1p8_current',
        start = 360*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current 1.8V (ADC 8)',
        unit = 'mA',
        disp = 'obcHk1p8Current'),

    dict(
        name = 'obc_hk3p3_current',
        start = 376*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current 3.3V (ADC 7)',
        unit = 'mA',
        disp = 'obcHk3p3Current'),

    dict(
        name = 'obc_hk1p0_voltage',
        start = 392*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage 1.0V (ADC 6)',
        unit = 'mV',
        disp = 'obcHk1p0Voltage'),

    dict(
        name = 'obc_hk1p8_voltage',
        start = 408*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage 1.8V (ADC 5)',
        unit = 'mV',
        disp = 'obcHk1p8Voltage'),

    dict(
        name = 'obc_hk2p5_voltage',
        start = 424*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage 2.5V (ADC 4)',
        unit = 'mV',
        disp = 'obcHk2p5Voltage'),

    dict(
        name = 'obc_hk3p3_voltage',
        start = 440*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage 3.3V (ADC 3)',
        unit = 'mV',
        disp = 'obcHk3p3Voltage'),

    dict(
        name = 'obc_hk3p3_voltage_in',
        start = 456*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage 3.3V in (ADC 2)',
        unit = 'mV',
        disp = 'obcHk3p3VoltageIn'),

    dict(
        name = 'obc_hk_temp',
        start = 472*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Temperature (ADC 1)',
        unit = 'degC',
        disp = 'obcHkTemp'),

    dict(
        name = 'obc_hk_reset_count',
        start = 488*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkResetCount'),

    dict(
        name = 'obc_hk_uptime',
        start = 520*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'IOBC uptime as measured by supervisor controller',
        unit = 's',
        disp = 'obcHkUptime'),

    dict(
        name = 'obc_hk_supervisor_uptime',
        start = 552*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Supervisor controller uptime',
        unit = 's',
        disp = 'obcHkSupervisorUptime'),

    dict(
        name = 'obc_hk_power_off_rtc',
        start = 585*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkPowerOffRtc'),

    dict(
        name = 'obc_hk_busy_rtc',
        start = 586*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkBusyRtc'),

    dict(
        name = 'obc_hk_is_in_supervisor_mode',
        start = 589*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkIsInSupervisorMode'),

    dict(
        name = 'obc_hk_power_rtc',
        start = 590*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkPowerRtc'),

    dict(
        name = 'obc_hk_power_obc',
        start = 591*b,
        l = 1*b,
        typ = 'bool',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkPowerObc'),

    dict(
        name = 'obc_hk_spi_command_status',
        start = 592*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkSpiCommandStatus'),

    dict(
        name = 'obc_hk_dummy',
        start = 600*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'obcHkDummy'),

    dict(
        name = 'eps_hk_reserved2',
        start = 608*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkReserved2'),

    dict(
        name = 'eps_hk_power_point_tracker_mode',
        start = 624*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkPowerPointTrackerMode'),

    dict(
        name = 'eps_hk_batt_mode',
        start = 632*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkBattMode'),

    dict(
        name = 'eps_hk_boot_cause',
        start = 640*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkBootCause'),

    dict(
        name = 'eps_hk_temp6',
        start = 648*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 6 (BP4b, BATT1)',
        unit = 'degC',
        disp = 'epsHkTemp6'),

    dict(
        name = 'eps_hk_temp5',
        start = 664*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 5 (BP4a, BATT0)',
        unit = 'degC',
        disp = 'epsHkTemp5'),

    dict(
        name = 'eps_hk_temp4',
        start = 680*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 4 (TEMP4)',
        unit = 'degC',
        disp = 'epsHkTemp4'),

    dict(
        name = 'eps_hk_temp3',
        start = 696*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 3 (TEMP3)',
        unit = 'degC',
        disp = 'epsHkTemp3'),

    dict(
        name = 'eps_hk_temp2',
        start = 712*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 2 (TEMP2)',
        unit = 'degC',
        disp = 'epsHkTemp2'),

    dict(
        name = 'eps_hk_temp1',
        start = 728*b,
        l = 16*b,
        typ = 'sint',
        verbose = 'Temperature sensor 1 (TEMP1)',
        unit = 'degC',
        disp = 'epsHkTemp1'),

    dict(
        name = 'eps_hk_counter_boot',
        start = 744*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCounterBoot'),

    dict(
        name = 'eps_hk_counter_wdt_csp2',
        start = 776*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCounterWdtCsp2'),

    dict(
        name = 'eps_hk_counter_wdt_csp1',
        start = 808*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCounterWdtCsp1'),

    dict(
        name = 'eps_hk_counter_wdt_gnd',
        start = 840*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCounterWdtGnd'),

    dict(
        name = 'eps_hk_counter_wdt_i2c',
        start = 872*b,
        l = 32*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCounterWdtI2c'),

    dict(
        name = 'eps_hk_wdt_csp_pings_left2',
        start = 904*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkWdtCspPingsLeft2'),

    dict(
        name = 'eps_hk_wdt_csp_pings_left1',
        start = 912*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkWdtCspPingsLeft1'),

    dict(
        name = 'eps_hk_wdt_gnd_time_left',
        start = 920*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Time left on ground watchdog',
        unit = 's',
        disp = 'epsHkWdtGndTimeLeft'),

    dict(
        name = 'eps_hk_wdt_i2c_time_left',
        start = 952*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Time left on I2C watchdog',
        unit = 's',
        disp = 'epsHkWdtI2cTimeLeft'),

    dict(
        name = 'eps_hk_latchup6',
        start = 984*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup6'),

    dict(
        name = 'eps_hk_latchup5',
        start = 1000*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup5'),

    dict(
        name = 'eps_hk_latchup4',
        start = 1016*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup4'),

    dict(
        name = 'eps_hk_latchup3',
        start = 1032*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup3'),

    dict(
        name = 'eps_hk_latchup2',
        start = 1048*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup2'),

    dict(
        name = 'eps_hk_latchup1',
        start = 1064*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkLatchup1'),

    dict(
        name = 'eps_hk_output_off_delta8',
        start = 1080*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 8 (BP4 switch)',
        unit = 's',
        disp = 'epsHkOutputOffDelta8'),

    dict(
        name = 'eps_hk_output_off_delta7',
        start = 1096*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 7 (BP4 heater)',
        unit = 's',
        disp = 'epsHkOutputOffDelta7'),

    dict(
        name = 'eps_hk_output_off_delta6',
        start = 1112*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 6',
        unit = 's',
        disp = 'epsHkOutputOffDelta6'),

    dict(
        name = 'eps_hk_output_off_delta5',
        start = 1128*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 5',
        unit = 's',
        disp = 'epsHkOutputOffDelta5'),

    dict(
        name = 'eps_hk_output_off_delta4',
        start = 1144*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 4',
        unit = 's',
        disp = 'epsHkOutputOffDelta4'),

    dict(
        name = 'eps_hk_output_off_delta3',
        start = 1160*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 3',
        unit = 's',
        disp = 'epsHkOutputOffDelta3'),

    dict(
        name = 'eps_hk_output_off_delta2',
        start = 1176*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 2',
        unit = 's',
        disp = 'epsHkOutputOffDelta2'),

    dict(
        name = 'eps_hk_output_off_delta1',
        start = 1192*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power off for channel 1',
        unit = 's',
        disp = 'epsHkOutputOffDelta1'),

    dict(
        name = 'eps_hk_output_on_delta8',
        start = 1208*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 8 (BP4 switch)',
        unit = 's',
        disp = 'epsHkOutputOnDelta8'),

    dict(
        name = 'eps_hk_output_on_delta7',
        start = 1224*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 7 (BP4 heater)',
        unit = 's',
        disp = 'epsHkOutputOnDelta7'),

    dict(
        name = 'eps_hk_output_on_delta6',
        start = 1240*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 6',
        unit = 's',
        disp = 'epsHkOutputOnDelta6'),

    dict(
        name = 'eps_hk_output_on_delta5',
        start = 1256*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 5',
        unit = 's',
        disp = 'epsHkOutputOnDelta5'),

    dict(
        name = 'eps_hk_output_on_delta4',
        start = 1272*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 4',
        unit = 's',
        disp = 'epsHkOutputOnDelta4'),

    dict(
        name = 'eps_hk_output_on_delta3',
        start = 1288*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 3',
        unit = 's',
        disp = 'epsHkOutputOnDelta3'),

    dict(
        name = 'eps_hk_output_on_delta2',
        start = 1304*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 2',
        unit = 's',
        disp = 'epsHkOutputOnDelta2'),

    dict(
        name = 'eps_hk_output_on_delta1',
        start = 1320*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Time till power on for channel 1',
        unit = 's',
        disp = 'epsHkOutputOnDelta1'),

    dict(
        name = 'eps_hk_output8',
        start = 1336*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput8'),

    dict(
        name = 'eps_hk_output7',
        start = 1344*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput7'),

    dict(
        name = 'eps_hk_output6',
        start = 1352*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput6'),

    dict(
        name = 'eps_hk_output5',
        start = 1360*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput5'),

    dict(
        name = 'eps_hk_output4',
        start = 1368*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput4'),

    dict(
        name = 'eps_hk_output3',
        start = 1376*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput3'),

    dict(
        name = 'eps_hk_output2',
        start = 1384*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput2'),

    dict(
        name = 'eps_hk_output1',
        start = 1392*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkOutput1'),

    dict(
        name = 'eps_hk_cur_out6',
        start = 1400*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 6',
        unit = 'mA',
        disp = 'epsHkCurOut6'),

    dict(
        name = 'eps_hk_cur_out5',
        start = 1416*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 5',
        unit = 'mA',
        disp = 'epsHkCurOut5'),

    dict(
        name = 'eps_hk_cur_out4',
        start = 1432*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 4',
        unit = 'mA',
        disp = 'epsHkCurOut4'),

    dict(
        name = 'eps_hk_cur_out3',
        start = 1448*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 3',
        unit = 'mA',
        disp = 'epsHkCurOut3'),

    dict(
        name = 'eps_hk_cur_out2',
        start = 1464*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 2',
        unit = 'mA',
        disp = 'epsHkCurOut2'),

    dict(
        name = 'eps_hk_cur_out1',
        start = 1480*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out 1',
        unit = 'mA',
        disp = 'epsHkCurOut1'),

    dict(
        name = 'eps_hk_reserved1',
        start = 1496*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkReserved1'),

    dict(
        name = 'eps_hk_cur_sys',
        start = 1512*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current out of the battery',
        unit = 'mA',
        disp = 'epsHkCurSys'),

    dict(
        name = 'eps_hk_cur_sun',
        start = 1528*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current from boost converters',
        unit = 'mA',
        disp = 'epsHkCurSun'),

    dict(
        name = 'eps_hk_cur_in3',
        start = 1544*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current in 3',
        unit = 'mA',
        disp = 'epsHkCurIn3'),

    dict(
        name = 'eps_hk_cur_in2',
        start = 1560*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current in 2',
        unit = 'mA',
        disp = 'epsHkCurIn2'),

    dict(
        name = 'eps_hk_cur_in1',
        start = 1576*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Current in 1',
        unit = 'mA',
        disp = 'epsHkCurIn1'),

    dict(
        name = 'eps_h_kv_batt',
        start = 1592*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage of battery',
        unit = 'mV',
        disp = 'epsHKvBatt'),

    dict(
        name = 'eps_h_kv_boost3',
        start = 1608*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage of boost converters for PV3',
        unit = 'mV',
        disp = 'epsHKvBoost3'),

    dict(
        name = 'eps_h_kv_boost2',
        start = 1624*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage of boost converters for PV2',
        unit = 'mV',
        disp = 'epsHKvBoost2'),

    dict(
        name = 'eps_h_kv_boost1',
        start = 1640*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Voltage of boost converters for PV1',
        unit = 'mV',
        disp = 'epsHKvBoost1'),

    dict(
        name = 'eps_hk_command_reply',
        start = 1656*b,
        l = 16*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'epsHkCommandReply'),

]

