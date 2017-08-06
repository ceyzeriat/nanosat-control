#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.utils import bincore
from ctrl.utils import b
from ctrl.utils import O


L1HK_KEYS = [
    dict(
        name = 'state_uart_dir',
        start = 0*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'stateUartDir'),

    dict(
        name = 'state_uart_write',
        start = 8*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'stateUartWrite'),

    dict(
        name = 'state_uart_read',
        start = 16*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'stateUartRead'),

    dict(
        name = 'tm_trxvu_buffer',
        start = 24*b,
        l = 8*b,
        typ = 'uint',
        verbose = 'Trxvu TmBuffer AvailFrames',
        unit = 'TmPackets',
        disp = 'tmTrxvuBuffer'),

    dict(
        name = 'tc_trxvu_buffer',
        start = 32*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Trxvu TcBuffer FrameCount',
        unit = 'TcPackets',
        disp = 'tcTrxvuBuffer'),

    dict(
        name = 'tm_l0_in_fifo',
        start = 48*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet L0ComManager fifo to ground',
        unit = 'TmPackets',
        disp = 'tmL0InFifo'),

    dict(
        name = 'l1_to_ground2_in_fifo',
        start = 64*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in buffer2 for ground',
        unit = 'TmPackets',
        disp = 'l1ToGround2InFifo'),

    dict(
        name = 'l1_to_ground1_in_fifo',
        start = 80*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in buffer1 for ground',
        unit = 'TmPackets',
        disp = 'l1ToGround1InFifo'),

    dict(
        name = 'techno_pld_in_fifo',
        start = 96*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in PldTechno',
        unit = 'TmPackets',
        disp = 'technoPldInFifo'),

    dict(
        name = 'processed_in_fifo',
        start = 112*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in Fifo with processed data',
        unit = 'TmPackets',
        disp = 'processedInFifo'),

    dict(
        name = 'raw_science1_in_fifo',
        start = 128*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in rawscience fifo',
        unit = 'TmPackets',
        disp = 'rawScience1InFifo'),

    dict(
        name = 'raw_science2_in_fifo',
        start = 144*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in temporary science fifo',
        unit = 'TmPackets',
        disp = 'rawScience2InFifo'),

    dict(
        name = 'hk_pld_in_fifo',
        start = 160*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in PldHKFifo',
        unit = 'TmPackets',
        disp = 'hkPldInFifo'),

    dict(
        name = 'hk_l1_in_fifo',
        start = 176*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Number of Packet in L1HKFifo',
        unit = 'TmPackets',
        disp = 'hkL1InFifo'),

    dict(
        name = 'bad_high',
        start = 192*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'High part of SD Card if greater than 4GB',
        unit = 'bytes',
        disp = 'bad_high'),

    dict(
        name = 'bad',
        start = 224*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Bad bytes on the SD Card.',
        unit = 'bytes',
        disp = 'bad'),

    dict(
        name = 'used_high',
        start = 256*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'High part of SD Card if greater than 4GB',
        unit = 'bytes',
        disp = 'used_high'),

    dict(
        name = 'used',
        start = 288*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Used bytes on the SD Card.',
        unit = 'bytes',
        disp = 'used'),

    dict(
        name = 'free_high',
        start = 320*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'High part of SD Card if greater than 4GB',
        unit = 'bytes',
        disp = 'free_high'),

    dict(
        name = 'free',
        start = 352*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Free bytes on the SD Card.',
        unit = 'bytes',
        disp = 'free'),

    dict(
        name = 'total_high',
        start = 384*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'High part of SD Card if greater than 4GB',
        unit = 'bytes',
        disp = 'total_high'),

    dict(
        name = 'total',
        start = 416*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Total size in bytes of the SD Card.',
        unit = 'bytes',
        disp = 'total'),

]

