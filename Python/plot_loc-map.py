""" Plot earthquake location distribution in map view
"""
import sys
sys.path.append('/home/zhouyj/software/data_prep')
from obspy import UTCDateTime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from reader import read_fctlg_np, slice_ctlg, read_fault
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlg = 'input/fctlg_eg.csv'
ffault = 'input/faults_eg.dat'
title = 'Example Map-view Location Plot'
fout = 'output/eg_loc-map.pdf'
# slicing criteria
ot_rng = '20190704-20190725'
ot_rng = [UTCDateTime(date) for date in ot_rng.split('-')]
lon_rng =  [-117.85, -117.25]
lat_rng = [35.45, 36.05]
dep_rng = [0, 15]
mag_rng = [-1,8]
mag_corr = 1. # avoid neg
# fig config
fig_size = (10*0.8, 11*0.8)
fsize_label = 12
fsize_title = 16
alpha = 0.6
cmap = plt.get_cmap('hot')
mark_size = 2. # seismic events
line_wid = 1. # fault trace
plt_style = ['ggplot',None][1]
bg_color = 'darkgray'
grid_color = 'lightgray'
cbar_pos = [0.16,0.1,0.03,0.25]
cbar_ticks = np.arange(0,1.1,0.333)
cbar_tlabels = ['15','10','5','0']

def read_catalog(fctlg):
    events = read_fctlg_np(fctlg)
    events['mag'] += mag_corr
    events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng, ot_rng=ot_rng)
    events = np.sort(events, order='ot')
    print('%s %s events'%(fctlg,len(events)))
    lat = np.array(list(events['lat']))
    lon = np.array(list(events['lon']))
    dep = np.array(list(events['dep']))
    mag = np.array(list(events['mag'])) * mark_size
    return lat, lon, dep, mag

def plot_label(xlabel=None, ylabel=None, title=None):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

if plt_style: plt.style.use(plt_style)
fig = plt.figure(figsize=fig_size)
ax = plt.gca()
ax.set_facecolor(bg_color)
tr0 = ax.transData
# fill up edge
edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]]
edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
# plot seis events
lat, lon, dep, mag = read_catalog(fctlg)
color = [cmap(1-(di-dep_rng[0])/(dep_rng[1]-dep_rng[0])) for di in dep]
plt.scatter(lon, lat, mag, alpha=alpha, color=color, edgecolor='none', zorder=len(faults)+1)
# plot faults
faults = read_fault(ffault, lat_rng, lon_rng)
for fault in faults: 
    plt.plot(fault[:,0], fault[:,1], color='gray', linewidth=line_wid, zorder=2)
plt.grid(True, color=grid_color, zorder=1)
plot_label(title=title)
# plot colorbar
cbar_ax = fig.add_axes(cbar_pos)
cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
cbar.set_label('Depth (km)', rotation=-90, va="bottom", fontsize=fsize_label)
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tlabels)
# save fig
plt.tight_layout()
plt.savefig(fout)
