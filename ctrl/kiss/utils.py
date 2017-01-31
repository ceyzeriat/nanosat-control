#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import constants
from ..utils import core


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
    callsign = core.str2bytes(callsign).lstrip().rstrip()

    if b'-' in callsign:
        if not callsign.count(b'-') == 1:
            return False
        else:
            callsign, ssid = callsign.split(b'-')
    else:
        ssid = b'0'

    # Test length, call should be 2--6
    if not ((2 <= len(callsign) <= 6) and (1 <= len(ssid) <= 2)):
        return False

    for char in callsign:
        if not (str(char).isalpha() or str(char).isdigit()):
            if not (char == b'*' and callsign[-1] == b'*'):
                return False

    if not str(ssid).isdigit():
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





def extract_ui(frame):
    """
    Extracts the UI component of an individual frame.

    :param frame: AX.25 frame.
    :type frame: str
    :returns: UI component of frame.
    :rtype: str
    """
    start_ui = frame.split(
        b''.join([constants.FEND, constants.DATA_FRAME]))
    end_ui = start_ui[0].split(''.join([constants.SLOT_TIME, '\xf0']))
    return ''.join([chr(ord(x) >> 1) for x in end_ui[0]])


def strip_nmea(frame):
    """
    Extracts NMEA header from T3-Micro or NMEA encoded KISS frames.
    """
    if len(frame) > 0:
        if ord(frame[0]) == 240:
            return frame[1:].rstrip()
    return frame


