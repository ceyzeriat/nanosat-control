#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from ctrl.utils import core
from ctrl import antenna


print("Initialization...")
antenna.init_antenna()

print("Starting...")
while 1:
    time.sleep(1./core.ANTENNARPORTREADFREQ)
    n = antenna.ANTENNA.in_waiting()
    if n > 0:
        # grab data
        data = antenna.ANTENNA.read(size=n)
        # deal with it in a separate thread
        loopy = Thread(target=antenna.process_data, args=(data, ))
        loopy.daemon = True
        loopy.start()
