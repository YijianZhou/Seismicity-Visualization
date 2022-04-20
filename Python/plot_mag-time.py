""" plot Magnitue-Time sequence
"""
import sys
sys.path.append('/home/zhouyj/software/data_prep')
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime
from reader import read_fctlg_np, slice_ctlg

# i/o paths
fctlg = 'input/fctlg_eg.csv'
title = 'Example Magnitude-Time Sequence'
fout = 'output/eg_mag-time.pdf'
# slicing criteria
ot_rng = '20210517-20210530'
ot_rng = [UTCDateTime(time) for time in ot_rng.split('-')]
lon_rng = [102.2, 102.35]
lat_rng = [29.125, 29.275]
dep_rng = [5, 15]
mag_rng = [-1, 4.2]
# fig config
alpha = 0.6
marker_size = 10
fig_size = (16*0.8,9*0.8)
fsize_label = 14
fsize_title= 18

def plot_label(xlabel=None, ylabel=None, title=None):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# read catalog
events = read_fctlg_np(fctlg)
events = slice_ctlg(events, ot_rng=ot_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng)
mag = list(events['mag'])
ot = [ti.datetime for ti in events['ot']]

plt.figure(figsize=fig_size)
plt.scatter(ot, mag, marker_size*np.ones(len(mag)), edgecolor='none', alpha=alpha)
plt.scatter(ot[0:2], np.array(mag_rng), alpha=0) # fill edge
plot_label(None, 'Magnitude', title)
plt.tight_layout()
plt.savefig(fout)
