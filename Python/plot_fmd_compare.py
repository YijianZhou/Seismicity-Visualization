""" Plot comparison of FMD between catalogs
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from reader import read_ctlg, read_fault, slice_ctlg, slice_ctlg_circle
from statis_lib import calc_fmd
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlgs = ['input/catalog_example1.csv','input/catalog_example2.csv']
names = ['Catalog1','Catalog2']
colors = ['tab:blue', 'tab:orange']
title = 'Example FMD Comparison'
fout = 'output/example_fmd_compare.pdf'
# catalog info
lon_rng =  [-117.9, -117.2]
lat_rng = [35.4, 36.1]
dep_rng = [0, 20]
mag_rng = [-1, 8]
# fig params
fig_size = (8,6)
fsize_label = 14
fsize_title = 18
mark_size = 10.
alpha = 0.6
mark_non_cum = '^'
mark_cum = '.'

# read catalog
mags = []
for fctlg in fctlgs:
    events = read_ctlg(fctlg)
    events = slice_ctlg(events, mag_rng=mag_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    mags.append(np.array(list(events['mag'])))

# start plot
plt.figure(figsize=fig_size)
p_list = []
for i in range(len(fctlgs)):
    mag_bin, num, cum_num = calc_fmd(mags[i])
    p_i = plt.semilogy(mag_bin, num, mark_non_cum, markersize=mark_size, color=colors[i], alpha=alpha)
    p_i+= plt.semilogy(mag_bin, cum_num, mark_cum, markersize=mark_size, color=colors[i], alpha=alpha)
    p_list.append(p_i[0])
plt.legend(p_list, names, fontsize=fsize_label)
plt.xlabel('Magnitude', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
ax = plt.gca()
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig(fout)
plt.show()
