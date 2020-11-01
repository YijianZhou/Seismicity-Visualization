""" plot M-T
"""
import sys
sys.path.append('/home/zhouyj/software/seis_view')
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime
from reader import read_ctlg, slice_ctlg
from statis_lib import gr_fit, calc_fmd

# i/o paths
fctlg = 'input/catalog_example.csv'
title = 'Example Magnitude-Time Sequence'
fout = 'output/example_mag_time.pdf'
lon_rng = [102.2, 102.35]
lat_rng = [29.125, 29.275]
dep_rng = [5, 15]
mag_corr = 1.
dep_corr = 0
mag_rng = [-1, 4.2]
# fig params
alpha = 0.6
mark_size = 8
fig_size = (16*0.8,9*0.8)
fsize_label = 14
fsize_title= 18

# read catalog
events = read_ctlg(fctlg)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng)
mag = np.array(list(events['mag']))
ot = [oti.datetime for oti in events['ot']]

# start plotting
plt.figure(figsize=fig_size)
ax=plt.gca()
plt.scatter(ot, mag, mark_size*np.ones(len(mag)), alpha=alpha)
# fill edge
plt.scatter(ot[0:2], mag_rng, alpha=0)
# plot title & label
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=20)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.ylabel('Magnitude', fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig(fout)
plt.show()
