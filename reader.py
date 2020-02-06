""" File reader
"""
import os
import numpy as np
from obspy import UTCDateTime


def read_ctlg(fctlg):
    dtype = [('ot','O'),('lat','O'),('lon','O'),('dep','O'),('mag','O')]
    f=open(fctlg); lines=f.readlines(); f.close()
    out = []
    for line in lines:
        codes = line.split(',')
        ot = UTCDateTime(codes[0])
        lat, lon, dep, mag = [float(code) for code in codes[1:]]
        out.append((ot, lat, lon, dep, mag))
    return np.array(out, dtype=dtype)


