""" Plot depth histogram comparison
"""
import sys
sys.path.append('/home/zhouyj/software/data_prep')
import numpy as np
import matplotlib.pyplot as plt
from reader import read_fctlg_np, read_fault, slice_ctlg, slice_ctlg_circle
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlgs = ['input/fctlg_eg1.csv','input/fctlg_eg2.csv']
names = ['Catalog 1','Catalog 2']
colors = ['tab:blue','tab:orange']
title = 'Example Depth Comparison'
fout = 'output/eg_dep-compare.pdf'
# slicing criteria
lon_rng =  [101.05,103.5]
lat_rng = [27.1,30.25]
dep_rng = [0, 30]
mag_rng = [-1,8]
bins = np.arange(0,30.1,3)
# fig config
fig_size = (8,6)
fsize_label = 14
fsize_title = 18
alpha = 0.6

def plot_label(xlabel=None, ylabel=None, title=None):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# read catalog
deps = []
for fctlg in fctlgs:
    events = read_fctlg_np(fctlg)
    events = slice_ctlg(events, mag_rng=mag_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    deps.append(np.array(list(events['dep'])))

# start plot
plt.figure(figsize=fig_size)
ax = plt.gca()
for i in range(len(fctlgs)):
    plt.hist(deps[i], bins, edgecolor='tab:gray', alpha=alpha, label=names[i])
ax.legend(fontsize=fsize_label)
plot_label('Depth (km)', 'Number', title)
plt.tight_layout()
plt.savefig(fout)
