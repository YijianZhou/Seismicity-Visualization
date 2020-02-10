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


def slice_ctlg(events, ot_rng=None, lat_rng=None, lon_rng=None, dep_rng=None, mag_rng=None):
    if ot_rng: events = events[(events['ot']>ot_rng[0])*(events['ot']<ot_rng[1])]
    if lat_rng: events = events[(events['lat']>lat_rng[0])*(events['lat']<lat_rng[1])]
    if lon_rng: events = events[(events['lon']>lon_rng[0])*(events['lon']<lon_rng[1])]
    if dep_rng: events = events[(events['dep']>dep_rng[0])*(events['dep']<dep_rng[1])]
    if mag_rng: events = events[(events['mag']>mag_rng[0])*(events['mag']<mag_rng[1])]
    return events

