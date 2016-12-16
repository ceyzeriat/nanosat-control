#!/usr/bin/env python
# -*- coding: utf-8 -*-


MINLENPARAMSTRUCTURE = 3


echo = {'number':1,
        'name': 'echo',
        'level': 0,
        'subsystem': '',
        'apid':  'L0ComManager',
        'desc': "Picsat receives a message (2 chars) and replies with the same message",
        'lparam': 2,
        'param': (('message', 'the message', (0, 255), 'str', 2, None), )}
