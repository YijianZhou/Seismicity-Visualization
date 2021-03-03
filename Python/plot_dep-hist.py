""" Plot depth histogram
"""
import sys
sys.path.append('/home/zhouyj/software/seis_view')
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from reader import read_ctlg, read_fault, slice_ctlg, slice_ctlg_circle
from statis_lib import calc_fmd
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlgs = ['input/example1.ctlg','input/example2.ctlg']
names = ['Catalog 1','Catalog 2']
colors = ['tab:blue','tab:orange']
title = 'Seismicity Depth Distribution'
fout = 'output/example_dep-hist.pdf'
# catalog info
lon_rng =  [101.05,103.5]
lat_rng = [27.1,30.25]
dep_rng = [0, 30]
mag_rng = [-1,8]
bins = np.arange(0,30.1,3)
# fig params
fig_size = (8,6)
fsize_label = 14
fsize_title = 18
mark_size = 10.
alpha = 0.6

# read catalog
deps = []
for fctlg in fctlgs:
    events = read_ctlg(fctlg)
    events = slice_ctlg(events, mag_rng=mag_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    deps.append(np.array(list(events['dep'])))

# start plot
plt.figure(figsize=fig_size)
ax = plt.gca()
for i in range(len(fctlgs)):
    plt.hist(deps[i], bins, edgecolor='tab:gray', alpha=alpha, label=names[i])
ax.legend(fontsize=fsize_label)
# title & label
plt.xlabel('Depth (km)', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
# finish plot
plt.tight_layout()
plt.savefig(fout)
