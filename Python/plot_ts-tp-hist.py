""" Histogram of ts-tp 
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np

# i/o paths
fpha = 'input/fpha_eg.csv'
fout = 'output/eg_ts-tp-hist.pdf'
title = 'Example ts-tp Histogram'
# fig config
fig_size = (8,6)
fsize_label = 12
fsize_title = 16
max_dt = 15
bins = np.arange(0,max_dt+.1,1.)

def plot_label(xlabel=None, ylabel=None, title=None):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# read fpha
ts_tp = []
f=open(fpha); lines=f.readlines(); f.close()
for line in lines:
    codes = line.split(',')
    if len(codes[0])>10: continue
    tp, ts = [UTCDateTime(code) for code in codes[1:3]]
    ti = ts - tp
    if 0<ti<max_dt: ts_tp.append(ti)

plt.figure(figsize=fig_size)
ax = plt.gca()
plt.hist(ts_tp, bins=bins, edgecolor='tab:gray', alpha=0.8)
plot_label('ts - tp (sec)', 'Number of Picks', title)
plt.tight_layout()
plt.savefig(fout)
