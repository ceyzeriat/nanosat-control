#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":

    from ctrl.utils import core
    from segsol import spying

    dir_name = raw_input('Name of the directory where to save TM_DATA: ')

    core.prepare_terminal('Spy')
    print("Initialization...")
    spying.init(dir_name)
    print("Spying...")
