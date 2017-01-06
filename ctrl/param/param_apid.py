#!/usr/bin/env python
# -*- coding: utf-8 -*-


# taken from https://nubes-lesia.obspm.fr/index.php/apps/files?dir=%2FPicSat%2FProjet%2FtrxDoc


PIDREGISTRATION_OBC_L0 = {  'L0ComManager': 0,
                            'MemoryManager': 1,
                            'Housekeeper': 2,
                            'L0EventProcessor': 3,
                            'EpsManager': 4,
                            'L0AdcsManager': 5}

PIDREGISTRATION_OBC_L1 = {  'L1ComManager': 0,
                            'L1EventManager': 1,
                            'L1AdcsManager': 2,
                            'ModeManager': 3,
                            'EventManager': 4,
                            'payloadManager1': 6,
                            'payloadManager2': 7,
                            'payloadManager3': 8}

PIDREGISTRATION_PLD = {     'hkPayload': 2,
                            'sciencePayload': 3,
                            'debugPayload': 4}


PIDREGISTRATION = {}
PLDREGISTRATION = {}
LVLREGISTRATION = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '0'
    LVLREGISTRATION[k] = '0'

for k, v in PIDREGISTRATION_OBC_L1.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '0'
    LVLREGISTRATION[k] = '1'

for k, v in PIDREGISTRATION_PLD.items():
    PIDREGISTRATION[k] = v
    PLDREGISTRATION[k] = '1'


# PIDREGISTRATION_REV[pld][lvl]

PIDREGISTRATION_REV = {}
for k, v in PIDREGISTRATION_OBC_L0.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][0] = k

for k, v in PIDREGISTRATION_OBC_L1.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][0][1] = k

for k, v in PIDREGISTRATION_PLD.items():
    if not v in PIDREGISTRATION_REV.keys():
        PIDREGISTRATION_REV[v] = [['', ''], ['', '']]
    PIDREGISTRATION_REV[v][1][0] = k
