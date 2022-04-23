""" plot Magnitue-Time sequence & seismic rate
"""
import sys
sys.path.append('/home/zhouyj/software/data_prep')
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from obspy import UTCDateTime
from reader import read_fctlg_np, slice_ctlg

# i/o paths
fctlg = 'input/fctlg_eg1.csv'
title = 'Example Magnitude-Time Sequence'
fout = 'output/eg_mag-time.pdf'
# slicing criteria
ot_rng = '20190704-20190710'
ot_rng = [UTCDateTime(date) for date in ot_rng.split('-')]
lon_rng =  [-117.85, -117.25]
lat_rng = [35.45, 36.05]
dep_rng = [0, 15]
mag_rng = [-0.2,7.5]
# calc seis rate
win_len = 4*3600 # sec
win_stride = 2*3600 
num_steps = int((ot_rng[1] - ot_rng[0] - win_len) / win_stride) + 1
time = [(ot_rng[0]+win_len/2+win_stride*i).datetime for i in range(num_steps)]
num_workers = 10
# fig config
alpha = 0.6
marker_size = 10
fig_size = (16*0.8,9*0.8)
fsize_label = 14
fsize_title= 18

def plot_label(xlabel=None, ylabel=None, title=None, xrot=0):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=xrot)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# read catalog
events = read_fctlg_np(fctlg)
events = slice_ctlg(events, ot_rng=ot_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng)
mag = list(events['mag'])
ot = events['ot']
ot_plot = [oti.datetime for oti in ot]

# calc seismic rate
def calc_rate(win_idx):
    ot_min = ot_rng[0] + win_idx*win_stride
    ot_max = ot_rng[0] + win_idx*win_stride + win_len
    return sum((ot-ot_min>0)*(ot-ot_max<0)) / (win_len/3600)

pool = mp.Pool(num_workers)
mp_out = pool.map_async(calc_rate, range(num_steps))
pool.close()
pool.join()
seis_rate = mp_out.get()

plt.figure(figsize=fig_size)
# 1. plot M-T
ax = plt.gca()
plt.scatter(ot_plot, mag, marker_size*np.ones(len(mag)), edgecolor='none', alpha=alpha)
plt.scatter(ot_plot[0:2], np.array(mag_rng), alpha=0) # fill edge
plot_label(None, 'Magnitude', title, xrot=20)
# 2. plot seis rate
ax = ax.twinx()
plt.plot(time, seis_rate, color='red', alpha=0.8)
plot_label(None, 'Seismic Rate (/hour)', None, 20)
plt.annotate('window length = %shr\nstep stride = %shr'%(int(win_len/3600), int(win_stride/3600)),
    (time[-1],np.amax(seis_rate)), ha='right', va='top', fontsize=fsize_label)
ax.set_ylabel('Seismic Rate (/hour)', fontsize=fsize_label, color='red', rotation=-90, va='bottom')
ax.tick_params(axis='y', colors='red', labelsize=fsize_label)
plt.tight_layout()
plt.savefig(fout)
