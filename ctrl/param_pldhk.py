#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .ccsds.ccsdskey import CCSDSKey
from . import core


# fonctions de conversion des HK payload depuis des valeurs hex
def voltage_line_5V_fct(hx):
    return 4.59e-3 * core.hex2int(hx)

def current_lines_fct(hx):
    return 1.61e-3 * core.hex2int(hx)

def temp_fct(hx):
    return 0.0625 * core.hex2int(hx)

def voltage_piezo_fct(hx):
    return 3.3 * 213.77 / 4096.0 * core.hex2int(hx)

def current_peizo_fct(hx):
    return 0.00161 * core.hex2int(hx)

def voltage_peltier_fct(hx):
    return 3.3 / 4096.0 * core.hex2int(hx)

def voltage_peltier_error_fct(hx, hx_vref_raw):
    return 3.3 / 25.0 / 4096.0 * (core.hex2int(hx) - core.hex2int(hx_vref_raw))

def current_peltier_fct(hx, hx_vref_raw):
    return 3300.0 / 0.16 / 4096.0 * (core.hex2int(hx) - core.hex2int(hx_vref_raw))

def temp_diode_fct(hx, hx_vref_raw):
    hxint = core.hex2int(hx)
    return 293.0 / (293.0 / 2918.9 * np.log(50.0 * hxint / (11.0* (core.hex2int(hx_vref_raw) - hxint))) + 1.0) - 273.15

def mask_sensor_fct(hx):
    bits = list("".join([core.hex2bin(item, pad=False) for item in hx])[:SENSORCOUNT])
    return list(map(bool, map(int, bits)))


# data
# origin of start/end is end of secondary header
# start/end units is octet

SENSORCOUNT = 12

SENSORMASK = CCSDSKey('SENSORMASK', start=0, l=2, fct=mask_sensor)

VOLTAGELINE5V = CCSDSKey('voltage_lines_5V', start=2, l=2, fct=voltage_line_5V_fct)
CURRENTLINE5V = CCSDSKey('curernt_lines_5V', start=4, l=2, fct=current_lines_fct)
CURRENTLINE3V = CCSDSKey('current_lines_3V', start=6, l=2, fct=current_lines_fct)
VOLTAGEPIEZO = CCSDSKey('voltage_piezo', start=8, l=2, fct=voltage_piezo_fct)
CURRENTPIEZO = CCSDSKey('current_piezo', start=10, l=2, fct=current_peizo_fct)
CURRENTPELTIER = CCSDSKey('current_peltier', start=12, l=2, fct=current_peltier_fct)
TEMPDIODE = CCSDSKey('temp_diode', start=14, l=2, fct=temp_diode_fct)
VOLTAGEPELTIERERROR = CCSDSKey('voltage_peltier_error', start=16, l=2, fct=voltage_peltier_error_fct)
VOLTAGEPELTIER = CCSDSKey('voltage_peltier', start=18, l=2, fct=voltage_peltier_fct)
TEMP1 = CCSDSKey('temp1', start=20, l=2, fct=temp_fct)
TEMP2 = CCSDSKey('temp2', start=22, l=2, fct=temp_fct)
TEMP3 = CCSDSKey('temp3', start=24, l=2, fct=temp_fct)


DATA_KEYS = [SENSORMASK, VOLTAGELINE5V, CURRENTLINE5V, CURRENTLINE3V, VOLTAGEPIEZO, CURRENTPIEZO, CURRENTPELTIER, TEMPDIODE, VOLTAGEPELTIERERROR, VOLTAGEPELTIER, TEMP1, TEMP2, TEMP3]
