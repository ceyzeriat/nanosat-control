#!/usr/bin/env python
# -*- coding: utf-8 -*-


MINLENPARAMSTRUCTURE = 3


echo = {'number':1,
        'name': 'echo',
        'level': 0,
        'subsystem': '',
        'apid':  '',
        'desc': "Picsat receives the message (<=2 chars) and replies with the same message",
        'lparam': 2,
        'param': (('message', 'the message', (0, 255), 'str', 2, None), )}

autre = {'number':2,
         'name': 'autre',
         'level': 0,
         'subsystem': '',
         'apid':  '',
         'desc': "Picsat receives the message (<=2 chars) and replies with the same message",
         'lparam': 2,
         'param': (('message', 'the message', {'a': '\x01', 'b': '\x10'}, 'str', 1, None), )}
