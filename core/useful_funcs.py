#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
useful funcs core weeklysale
"""
DPI = 300
def pixtomm(pix):
    pix = float(pix)
    #print('hello',pix)
    mm = pix/DPI*25.4
    #print('hellomm',mm)
    return mm

def mmtopix(mm):
    mm = float(mm)
    pix = int( mm/25.4*DPI)
    return pix