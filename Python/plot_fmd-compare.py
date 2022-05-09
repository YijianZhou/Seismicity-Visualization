""" Plot comparison of FMD between catalogs
"""
import numpy as np
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from reader import read_fctlg, slice_ctlg
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlgs = ['input/fctlg_eg1.csv','input/fctlg_eg2.csv']
names = ['Catalog 1','Catalog 2']
colors = ['tab:blue', 'tab:orange']
zorders = [1,2]
title = 'Example FMD Comparison'
fout = 'output/eg_fmd-compare.pdf'
# slicing criteria
ot_rng = '20190704-20190710'
ot_rng = [UTCDateTime(date) for date in ot_rng.split('-')]
lon_rng =  [-117.9, -117.2]
lat_rng = [35.4, 36.1]
dep_rng = [0, 20]
mag_rng = [-1, 8]
# fig config
fig_size = (8,6)
fsize_label = 12
fsize_title = 16
marker_size = 10.
marker_non_cum = '^'
marker_cum = '.'
alpha = 0.6

def calc_fmd(mag):
    mag = mag[mag!=-np.inf]
    mag_max = np.ceil(10 * max(mag)) / 10
    mag_min = np.floor(10 * min(mag)) / 10
    mag_bin = np.around(np.arange(mag_min-0.1, mag_max+0.2, 0.1),1)
    num = np.histogram(mag, mag_bin)[0]
    cum_num = np.cumsum(num[::-1])[::-1]
    return mag_bin[1:], num, cum_num

def plot_label(xlabel=None, ylabel=None, title=None):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# read catalog
mags = []
for fctlg in fctlgs:
    events = read_fctlg(fctlg)
    events = slice_ctlg(events, ot_rng=ot_rng, mag_rng=mag_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    mags.append(np.array(list(events['mag'])))

# start plot
plt.figure(figsize=fig_size)
p_list = []
for i in range(len(fctlgs)):
    mag_bin, num, cum_num = calc_fmd(mags[i])
    p_i = plt.semilogy(mag_bin, num, marker_non_cum, markersize=marker_size, color=colors[i], markeredgecolor='gray', zorder=zorders[i], alpha=alpha)
    p_i+= plt.semilogy(mag_bin, cum_num, marker_cum, markersize=marker_size, color=colors[i], markeredgecolor='gray', zorder=zorders[i], alpha=alpha)
    p_list.append(p_i[0])
plt.legend(p_list, names, fontsize=fsize_label)
plot_label('Magnitude', 'Number', title)
plt.tight_layout()
plt.savefig(fout)
