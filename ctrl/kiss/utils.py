#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import constants
from ..utils import core
from ..utils import Byt


__all__ = ['escape_special_codes', 'valid_callsign', 'recover_special_codes',
            'strip_df_start',
            'extract_ui', 'strip_nmea']


def escape_special_codes(raw_codes):
    """
    Escape special codes, per KISS spec.

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    return raw_codes.replace(constants.FESC, constants.FESC_TFESC)\
                    .replace(constants.FEND, constants.FESC_TFEND)


def valid_callsign(callsign):
    """
    Validates callsign, returns bool.

    Args:
    * callsign (str): Callsign to validate
    """
    callsign = Byt(callsign).strip()

    if callsign.find(Byt('-')) != -1:
        if callsign.count(Byt('-')) == 1:
            callsign, ssid = callsign.split(Byt('-'))
        else:
            return False
    else:
        ssid = Byt('0')

    # Test length, call should be 2--6
    if not ((2 <= len(callsign) <= 6) and (1 <= len(ssid) <= 2)):
        return False

    for char in callsign:
        if not (char.isalpha() or char.isdigit()):
            if not (char == Byt("*") and callsign[-1] == Byt("*")):
                return False

    # conversion in number fails
    if not ssid.isdigit():
        return False

    if not (0 <= int(ssid) <= 15):
        return False

    return True


def strip_df_start(frame):
    """
    Strips KISS DATA_FRAME start (0x00) and newline from frame.

    :param frame: APRS/AX.25 frame.
    :type frame: str
    :returns: APRS/AX.25 frame sans DATA_FRAME start (0x00).
    :rtype: str
    """
    return frame.strip(constants.FEND).lstrip(constants.DATA_FRAME)


def recover_special_codes(escaped_codes):
    """
    Recover special codes, per KISS spec.

    "If the FESC_TFESC or FESC_TFEND escaped codes appear in the data received,
    they need to be recovered to the original codes. The FESC_TFESC code is
    replaced by FESC code and FESC_TFEND is replaced by FEND code."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    return escaped_codes.replace(constants.FESC_TFESC, constants.FESC)\
                        .replace(constants.FESC_TFEND, constants.FEND)
