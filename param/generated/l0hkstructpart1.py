
from ctrl.utils import bincore

L0HKSTRUCTPART1_KEYS = [
dict(
         name = 'fram_enable_error_flag',
         start = 1,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'framEnableErrorFlag'),

dict(
         name = 'ants_b_error_flag',
         start = 2,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsBErrorFlag'),

dict(
         name = 'ants_a_error_flag',
         start = 3,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsAErrorFlag'),

dict(
         name = 'trxvu_tx_error_flag',
         start = 4,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'trxvuTxErrorFlag'),

dict(
         name = 'trxvu_rx_error_flag',
         start = 5,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'trxvuRxErrorFlag'),

dict(
         name = 'obc_supervisor_error_flag',
         start = 6,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'obcSupervisorErrorFlag'),

dict(
         name = 'gom_eps_error_flag',
         start = 7,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'gomEpsErrorFlag'),

dict(
         name = 'ants_uptime_b',
         start = 8,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsUptimeB'),

dict(
         name = 'ant1_undeployed_ants_b_status',
         start = 40,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1UndeployedAntsBStatus'),

dict(
         name = 'ant1_timeout_ants_b_status',
         start = 41,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1TimeoutAntsBStatus'),

dict(
         name = 'ant1_deploying_ants_b_status',
         start = 42,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1DeployingAntsBStatus'),

dict(
         name = 'ant2_undeployed_ants_b_status',
         start = 44,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2UndeployedAntsBStatus'),

dict(
         name = 'ant2_timeout_ants_b_status',
         start = 45,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2TimeoutAntsBStatus'),

dict(
         name = 'ant2_deploying_ants_b_status',
         start = 46,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2DeployingAntsBStatus'),

dict(
         name = 'ignore_flag_ants_b_status',
         start = 47,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ignoreFlagAntsBStatus'),

dict(
         name = 'ant3_undeployed_ants_b_status',
         start = 48,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3UndeployedAntsBStatus'),

dict(
         name = 'ant3_timeout_ants_b_status',
         start = 49,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3TimeoutAntsBStatus'),

dict(
         name = 'ant3_deploying_ants_b_status',
         start = 50,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3DeployingAntsBStatus'),

dict(
         name = 'ant4_undeployed_ants_b_status',
         start = 52,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4UndeployedAntsBStatus'),

dict(
         name = 'ant4_timeout_ants_b_status',
         start = 53,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4TimeoutAntsBStatus'),

dict(
         name = 'ant4_deploying_ants_b_status',
         start = 54,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4DeployingAntsBStatus'),

dict(
         name = 'armed_ants_b_status',
         start = 55,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'armedAntsBStatus'),

dict(
         name = 'ants_temperature_b',
         start = 56,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsTemperatureB'),

dict(
         name = 'ants_uptime_a',
         start = 72,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsUptimeA'),

dict(
         name = 'ant1_undeployed_ants_a_status',
         start = 104,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1UndeployedAntsAStatus'),

dict(
         name = 'ant1_timeout_ants_a_status',
         start = 105,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1TimeoutAntsAStatus'),

dict(
         name = 'ant1_deploying_ants_a_status',
         start = 106,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant1DeployingAntsAStatus'),

dict(
         name = 'ant2_undeployed_ants_a_status',
         start = 108,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2UndeployedAntsAStatus'),

dict(
         name = 'ant2_timeout_ants_a_status',
         start = 109,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2TimeoutAntsAStatus'),

dict(
         name = 'ant2_deploying_ants_a_status',
         start = 110,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant2DeployingAntsAStatus'),

dict(
         name = 'ignore_flag_ants_a_status',
         start = 111,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ignoreFlagAntsAStatus'),

dict(
         name = 'ant3_undeployed_ants_a_status',
         start = 112,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3UndeployedAntsAStatus'),

dict(
         name = 'ant3_timeout_ants_a_status',
         start = 113,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3TimeoutAntsAStatus'),

dict(
         name = 'ant3_deploying_ants_a_status',
         start = 114,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant3DeployingAntsAStatus'),

dict(
         name = 'ant4_undeployed_ants_a_status',
         start = 116,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4UndeployedAntsAStatus'),

dict(
         name = 'ant4_timeout_ants_a_status',
         start = 117,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4TimeoutAntsAStatus'),

dict(
         name = 'ant4_deploying_ants_a_status',
         start = 118,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'ant4DeployingAntsAStatus'),

dict(
         name = 'armed_ants_a_status',
         start = 119,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'armedAntsAStatus'),

dict(
         name = 'ants_temperature_a',
         start = 120,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'antsTemperatureA'),

dict(
         name = 'tx_trxvu_hk_current',
         start = 136,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Tx Telemetry transmitter current',
         disp = 'txTrxvuHkCurrent'),

dict(
         name = 'tx_trxvu_hk_forwardpower',
         start = 152,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Tx Telemetry forward power',
         disp = 'txTrxvuHkForwardpower'),

dict(
         name = 'tx_trxvu_hk_pa_temp',
         start = 168,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Tx Telemetry power amplifier temperature',
         disp = 'txTrxvuHkPaTemp'),

dict(
         name = 'tx_trxvu_hk_tx_reflectedpower',
         start = 184,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Tx Telemetry reflected power',
         disp = 'txTrxvuHkTxReflectedpower'),

dict(
         name = 'rx_trxvu_hk_rssi',
         start = 200,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry rssi measurement',
         disp = 'rxTrxvuHkRssi'),

dict(
         name = 'rx_trxvu_hk_pa_temp',
         start = 216,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry power amplifier temperature',
         disp = 'rxTrxvuHkPaTemp'),

dict(
         name = 'rx_trxvu_hk_board_temp',
         start = 232,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry board temperature',
         disp = 'rxTrxvuHkBoardTemp'),

dict(
         name = 'rx_trxvu_hk_bus_volt',
         start = 248,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry bus voltage',
         disp = 'rxTrxvuHkBusVolt'),

dict(
         name = 'rx_trxvu_hk_rx_current',
         start = 264,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry receiver current',
         disp = 'rxTrxvuHkRxCurrent'),

dict(
         name = 'rx_trxvu_hk_rx_doppler',
         start = 280,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry receiver doppler',
         disp = 'rxTrxvuHkRxDoppler'),

dict(
         name = 'rx_trxvu_hk_tx_current',
         start = 296,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Rx Telemetry transmitter current',
         disp = 'rxTrxvuHkTxCurrent'),

dict(
         name = 'crc8',
         start = 312,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'CRC byte',
         disp = 'crc8'),

dict(
         name = 'obc_hk_adc_update_flag',
         start = 320,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Update Flag',
         disp = 'obcHkAdcUpdateFlag'),

dict(
         name = 'obc_hk_adc_data10',
         start = 328,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 10',
         disp = 'obcHkAdcData10'),

dict(
         name = 'obc_hk_adc_data09',
         start = 344,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 09',
         disp = 'obcHkAdcData09'),

dict(
         name = 'obc_hk_adc_data08',
         start = 360,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 08',
         disp = 'obcHkAdcData08'),

dict(
         name = 'obc_hk_adc_data07',
         start = 376,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 07',
         disp = 'obcHkAdcData07'),

dict(
         name = 'obc_hk_adc_data06',
         start = 392,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 06',
         disp = 'obcHkAdcData06'),

dict(
         name = 'obc_hk_adc_data05',
         start = 408,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 05',
         disp = 'obcHkAdcData05'),

dict(
         name = 'obc_hk_adc_data04',
         start = 424,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 04',
         disp = 'obcHkAdcData04'),

dict(
         name = 'obc_hk_adc_data03',
         start = 440,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 03',
         disp = 'obcHkAdcData03'),

dict(
         name = 'obc_hk_adc_data02',
         start = 456,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 02',
         disp = 'obcHkAdcData02'),

dict(
         name = 'obc_hk_adc_data01',
         start = 472,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'ADC Data channel 01',
         disp = 'obcHkAdcData01'),

dict(
         name = 'obc_hk_reset_count',
         start = 488,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'IOBC Reset Count',
         disp = 'obcHkResetCount'),

dict(
         name = 'obc_hk_uptime',
         start = 520,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'IOBC Uptime as measured by Supervisor Controller',
         disp = 'obcHkUptime'),

dict(
         name = 'obc_hk_supervisor_uptime',
         start = 552,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Supervisor Controller Uptime',
         disp = 'obcHkSupervisorUptime'),

dict(
         name = 'obc_hk_power_off_rtc',
         start = 585,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'obcHkPowerOffRtc'),

dict(
         name = 'obc_hk_busy_rtc',
         start = 586,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = '[NO DOC STRING], see OBC documentation',
         disp = 'obcHkBusyRtc'),

dict(
         name = 'obc_hk_is_in_supervisor_mode',
         start = 589,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Supervisor mode',
         disp = 'obcHkIsInSupervisorMode'),

dict(
         name = 'obc_hk_power_rtc',
         start = 590,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Output power to the RTC',
         disp = 'obcHkPowerRtc'),

dict(
         name = 'obc_hk_power_obc',
         start = 591,
         l = 1,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'OBC Power',
         disp = 'obcHkPowerObc'),

dict(
         name = 'obc_hk_spi_command_status',
         start = 592,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'SPI Command Status',
         disp = 'obcHkSpiCommandStatus'),

dict(
         name = 'obc_hk_dummy',
         start = 600,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Dummy byte',
         disp = 'obcHkDummy'),

dict(
         name = 'eps_hk_reserved2',
         start = 608,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Reserved for future use (2)',
         disp = 'epsHkReserved2'),

dict(
         name = 'eps_hk_power_point_tracker_mode',
         start = 624,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Mode of power point tracker',
         disp = 'epsHkPowerPointTrackerMode'),

dict(
         name = 'eps_hk_batt_mode',
         start = 632,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Mode for battery [0 = normal, 1 = undervoltage, 2 = overvoltage]',
         disp = 'epsHkBattMode'),

dict(
         name = 'eps_hk_boot_cause',
         start = 640,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Cause of last EPS reset',
         disp = 'epsHkBootCause'),

dict(
         name = 'eps_hk_temp6',
         start = 648,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 6 (BATT1)',
         disp = 'epsHkTemp6'),

dict(
         name = 'eps_hk_temp5',
         start = 664,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 5 (BATT0)',
         disp = 'epsHkTemp5'),

dict(
         name = 'eps_hk_temp4',
         start = 680,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 4 (TEMP4)',
         disp = 'epsHkTemp4'),

dict(
         name = 'eps_hk_temp3',
         start = 696,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 3 (TEMP3)',
         disp = 'epsHkTemp3'),

dict(
         name = 'eps_hk_temp2',
         start = 712,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 2 (TEMP2)',
         disp = 'epsHkTemp2'),

dict(
         name = 'eps_hk_temp1',
         start = 728,
         l = 16,
         fctunpack = bincore.bin2intSign,
         fctpack = bincore.intSign2bin,
         verbose = 'Temperature sensor 1 (TEMP1)',
         disp = 'epsHkTemp1'),

dict(
         name = 'eps_hk_counter_boot',
         start = 744,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of EPS reboots',
         disp = 'epsHkCounterBoot'),

dict(
         name = 'eps_hk_counter_wdt_csp2',
         start = 776,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of watchdog CSP reboots 2',
         disp = 'epsHkCounterWdtCsp2'),

dict(
         name = 'eps_hk_counter_wdt_csp1',
         start = 808,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of watchdog CSP reboots 1',
         disp = 'epsHkCounterWdtCsp1'),

dict(
         name = 'eps_hk_counter_wdt_gnd',
         start = 840,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of watchdog GND reboots',
         disp = 'epsHkCounterWdtGnd'),

dict(
         name = 'eps_hk_counter_wdt_i2c',
         start = 872,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of watchdog I2C reboots',
         disp = 'epsHkCounterWdtI2c'),

dict(
         name = 'eps_hk_wdt_csp_pings_left2',
         start = 904,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Pings left on CSP watchdog 2',
         disp = 'epsHkWdtCspPingsLeft2'),

dict(
         name = 'eps_hk_wdt_csp_pings_left1',
         start = 912,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Pings left on CSP watchdog 1',
         disp = 'epsHkWdtCspPingsLeft1'),

dict(
         name = 'eps_hk_wdt_gnd_time_left',
         start = 920,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time left on ground watchdog',
         disp = 'epsHkWdtGndTimeLeft'),

dict(
         name = 'eps_hk_wdt_i2c_time_left',
         start = 952,
         l = 32,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time left on I2C watchdog',
         disp = 'epsHkWdtI2cTimeLeft'),

dict(
         name = 'eps_hk_latchup6',
         start = 984,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 6',
         disp = 'epsHkLatchup6'),

dict(
         name = 'eps_hk_latchup5',
         start = 1000,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 5',
         disp = 'epsHkLatchup5'),

dict(
         name = 'eps_hk_latchup4',
         start = 1016,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 4',
         disp = 'epsHkLatchup4'),

dict(
         name = 'eps_hk_latchup3',
         start = 1032,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 3',
         disp = 'epsHkLatchup3'),

dict(
         name = 'eps_hk_latchup2',
         start = 1048,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 2',
         disp = 'epsHkLatchup2'),

dict(
         name = 'eps_hk_latchup1',
         start = 1064,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Number of latch-ups for channel 1',
         disp = 'epsHkLatchup1'),

dict(
         name = 'eps_hk_output_off_delta8',
         start = 1080,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 8',
         disp = 'epsHkOutputOffDelta8'),

dict(
         name = 'eps_hk_output_off_delta7',
         start = 1096,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 7',
         disp = 'epsHkOutputOffDelta7'),

dict(
         name = 'eps_hk_output_off_delta6',
         start = 1112,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 6',
         disp = 'epsHkOutputOffDelta6'),

dict(
         name = 'eps_hk_output_off_delta5',
         start = 1128,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 5',
         disp = 'epsHkOutputOffDelta5'),

dict(
         name = 'eps_hk_output_off_delta4',
         start = 1144,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 4',
         disp = 'epsHkOutputOffDelta4'),

dict(
         name = 'eps_hk_output_off_delta3',
         start = 1160,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 3',
         disp = 'epsHkOutputOffDelta3'),

dict(
         name = 'eps_hk_output_off_delta2',
         start = 1176,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 2',
         disp = 'epsHkOutputOffDelta2'),

dict(
         name = 'eps_hk_output_off_delta1',
         start = 1192,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power off for channel 1',
         disp = 'epsHkOutputOffDelta1'),

dict(
         name = 'eps_hk_output_on_delta8',
         start = 1208,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 8',
         disp = 'epsHkOutputOnDelta8'),

dict(
         name = 'eps_hk_output_on_delta7',
         start = 1224,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 7',
         disp = 'epsHkOutputOnDelta7'),

dict(
         name = 'eps_hk_output_on_delta6',
         start = 1240,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 6',
         disp = 'epsHkOutputOnDelta6'),

dict(
         name = 'eps_hk_output_on_delta5',
         start = 1256,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 5',
         disp = 'epsHkOutputOnDelta5'),

dict(
         name = 'eps_hk_output_on_delta4',
         start = 1272,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 4',
         disp = 'epsHkOutputOnDelta4'),

dict(
         name = 'eps_hk_output_on_delta3',
         start = 1288,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 3',
         disp = 'epsHkOutputOnDelta3'),

dict(
         name = 'eps_hk_output_on_delta2',
         start = 1304,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 2',
         disp = 'epsHkOutputOnDelta2'),

dict(
         name = 'eps_hk_output_on_delta1',
         start = 1320,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Time till power on for channel 1',
         disp = 'epsHkOutputOnDelta1'),

dict(
         name = 'eps_hk_output8',
         start = 1336,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 8',
         disp = 'epsHkOutput8'),

dict(
         name = 'eps_hk_output7',
         start = 1344,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 7',
         disp = 'epsHkOutput7'),

dict(
         name = 'eps_hk_output6',
         start = 1352,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 6',
         disp = 'epsHkOutput6'),

dict(
         name = 'eps_hk_output5',
         start = 1360,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 5',
         disp = 'epsHkOutput5'),

dict(
         name = 'eps_hk_output4',
         start = 1368,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 4',
         disp = 'epsHkOutput4'),

dict(
         name = 'eps_hk_output3',
         start = 1376,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 3',
         disp = 'epsHkOutput3'),

dict(
         name = 'eps_hk_output2',
         start = 1384,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 2',
         disp = 'epsHkOutput2'),

dict(
         name = 'eps_hk_output1',
         start = 1392,
         l = 8,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Status of output 1',
         disp = 'epsHkOutput1'),

dict(
         name = 'eps_hk_cur_out6',
         start = 1400,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 6[mA]',
         disp = 'epsHkCurOut6'),

dict(
         name = 'eps_hk_cur_out5',
         start = 1416,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 5[mA]',
         disp = 'epsHkCurOut5'),

dict(
         name = 'eps_hk_cur_out4',
         start = 1432,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 4[mA]',
         disp = 'epsHkCurOut4'),

dict(
         name = 'eps_hk_cur_out3',
         start = 1448,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 3[mA]',
         disp = 'epsHkCurOut3'),

dict(
         name = 'eps_hk_cur_out2',
         start = 1464,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 2[mA]',
         disp = 'epsHkCurOut2'),

dict(
         name = 'eps_hk_cur_out1',
         start = 1480,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out 1[mA]',
         disp = 'epsHkCurOut1'),

dict(
         name = 'eps_hk_reserved1',
         start = 1496,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Reserved for future use (1)',
         disp = 'epsHkReserved1'),

dict(
         name = 'eps_hk_cur_sys',
         start = 1512,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current out of battery',
         disp = 'epsHkCurSys'),

dict(
         name = 'eps_hk_cur_sun',
         start = 1528,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current from boost converters',
         disp = 'epsHkCurSun'),

dict(
         name = 'eps_hk_cur_in3',
         start = 1544,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current in 3[mA]',
         disp = 'epsHkCurIn3'),

dict(
         name = 'eps_hk_cur_in2',
         start = 1560,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current in 2[mA]',
         disp = 'epsHkCurIn2'),

dict(
         name = 'eps_hk_cur_in1',
         start = 1576,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Current in 1[mA]',
         disp = 'epsHkCurIn1'),

dict(
         name = 'eps_h_kv_batt',
         start = 1592,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Voltage of battery [mV]',
         disp = 'epsHKvBatt'),

dict(
         name = 'eps_h_kv_boost3',
         start = 1608,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Voltage of boost converters [mV] [PV3]',
         disp = 'epsHKvBoost3'),

dict(
         name = 'eps_h_kv_boost2',
         start = 1624,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Voltage of boost converters [mV] [PV2]',
         disp = 'epsHKvBoost2'),

dict(
         name = 'eps_h_kv_boost1',
         start = 1640,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Voltage of boost converters [mV] [PV1]',
         disp = 'epsHKvBoost1'),

dict(
         name = 'eps_hk_command_reply',
         start = 1656,
         l = 16,
         fctunpack = bincore.bin2int,
         fctpack = bincore.int2bin,
         verbose = 'Reply of the last command',
         disp = 'epsHkCommandReply'),

]
