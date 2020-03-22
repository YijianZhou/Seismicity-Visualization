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


def read_pad_det(fctlg):
    dtype = [('ot','O'),('lat','O'),('lon','O'),('mag','O')]
    f=open(fctlg); lines=f.readlines(); f.close()
    out = []
    for line in lines:
        codes = line.split(',')
        ot = UTCDateTime(codes[0])
        lat, lon, mag = [float(code) for code in codes[1:4]]
        out.append((ot, lat, lon, mag))
    return np.array(out, dtype=dtype)


def slice_ctlg(events, ot_rng=None, lat_rng=None, lon_rng=None, dep_rng=None, mag_rng=None):
    if ot_rng: events = events[(events['ot']>ot_rng[0])*(events['ot']<ot_rng[1])]
    if lat_rng: events = events[(events['lat']>lat_rng[0])*(events['lat']<lat_rng[1])]
    if lon_rng: events = events[(events['lon']>lon_rng[0])*(events['lon']<lon_rng[1])]
    if dep_rng: events = events[(events['dep']>dep_rng[0])*(events['dep']<dep_rng[1])]
    if mag_rng: events = events[(events['mag']>mag_rng[0])*(events['mag']<mag_rng[1])]
    return events


def slice_ctlg_circle(events, ref_lat, ref_lon, radius):
    return events[(events['lat']-ref_lat)**2 \
               + ((events['lon']-ref_lon) * np.cos(ref_lat*np.pi/180))**2 \
               < radius**2]


def read_fault(fpath, lat_rng, lon_rng):
    faults = []
    f=open(fpath, errors='replace'); lines=f.readlines(); f.close()
    for line in lines:
        if line[0]=='>': 
            if faults==[]: faults.append([])
            elif faults[-1]!=[]: faults.append([])
        elif line[0]!='#': 
            lon, lat = [float(code) for code in line.split()]
            if lon<lon_rng[0] or lon>lon_rng[1]: continue
            if lat<lat_rng[0] or lat>lat_rng[1]: continue
            faults[-1].append([lon, lat])
    if faults[-1]==[]: faults = faults[:-1]
    for i in range(len(faults)): faults[i] = np.array(faults[i])
    return np.array(faults)
