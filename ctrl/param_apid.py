#!/usr/bin/env python
# -*- coding: utf-8 -*-


# taken from https://nubes-lesia.obspm.fr/index.php/apps/files?dir=%2FPicSat%2FProjet%2FtrxDoc


APIDREGISTRATION_OBC_L0 = { 'L0ComManager': 0,
                            'MemoryManager': 1,
                            'Housekeeper': 2,
                            'L0EventProcessor': 3,
                            'EpsManager': 4,
                            'L0AdcsManager': 5}

APIDREGISTRATION_OBC_L1 = { 'L1ComManager': 0,
                            'L1EventManager': 1,
                            'L1AdcsManager': 2,
                            'ModeManager': 3,
                            'EventManager': 4,
                            'L1AdcsManager': 5,
                            'payloadManager1': 6,
                            'payloadManager2': 7,
                            'payloadManager3': 8}

APIDREGISTRATION_PLD = {    'hkPayload': 2,
                            'sciencePayload': 3,
                            'debugPayload': 4}
