#!/usr/bin/env python
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import nanoutils
    from nanoapps import spying

    dir_name = raw_input('Name of the directory where to save TM_DATA: ')

    nanoutils.prepare_terminal('Spy')
    print("Initialization...")
    spying.init(dir_name)
    print("Spying...")
