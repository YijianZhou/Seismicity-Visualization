""" Histogram of ts-tp, ttp & tts
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from reader import read_fsta, read_fpha
from signal_lib import calc_dist_km

# i/o paths
fpha = 'input/fpha_eg.csv'
fsta = 'input/fsta_eg.csv'
fout = 'output/eg_ts-tp-dist.pdf'
titles = ['(a) S-P Time ~ Hypo-distance','(b) Travel Time Curve']
sta_dict = read_fsta(fsta)
event_list = read_fpha(fpha)
# fig config
fig_size = (12,6)
fsize_label = 14
fsize_title = 18
max_dt = 15
bins = [50,50] # dist (km) & time (s)
norm = [LogNorm(),None][0]
cmaps = ['hot_r','Blues','Greens']
cmaps = [plt.get_cmap(cmap) for cmap in cmaps]
cax_rects = [[0.1,0.8,0.18,0.03],[0.6,0.8,0.18,0.03],[0.6,0.7,0.18,0.03]] # left, bottom, width, height

def plot_label(xlabel=None, ylabel=None, title=None):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# calc hypo-distance
dist_list, dt_list, ttp_list, tts_list = [], [], [], []
for event_loc, pick_dict in event_list:
    ot, lat, lon, dep = event_loc[0:4]
    for sta,[tp,ts] in pick_dict.items():
        dt, ttp, tts = ts-tp, tp-ot, ts-ot
        if not (0<dt<max_dt and sta in sta_dict): continue
        sta_lat, sta_lon, sta_ele = sta_dict[sta]
        dxy = calc_dist_km([lat,sta_lat],[lon,sta_lon])
        dz = dep + sta_ele/1e3
        dist = (dxy**2 + dz**2)**0.5
        dt_list.append(dt)
        dist_list.append(dist)
        ttp_list.append(ttp)
        tts_list.append(tts)

plt.figure(figsize=fig_size)
plt.subplot(121)
ax = plt.gca()
plt.hist2d(dist_list, dt_list, bins=bins, cmap=cmaps[0], norm=norm)
plot_label('Hypocentral Distance (km)', 'ts - tp (sec)', titles[0])
cax = plt.axes(cax_rects[0])
plt.colorbar(cax=cax, orientation='horizontal')
plt.setp(cax.xaxis.get_majorticklabels(), fontsize=fsize_label)
cax.set_xlabel('Number of Picks', fontsize=fsize_label)
plt.subplot(122)
ax = plt.gca()
_,_,_, im1 = plt.hist2d(dist_list, ttp_list, bins=bins, cmap=cmaps[1], norm=norm)
_,_,_, im2 = plt.hist2d(dist_list, tts_list, bins=bins, cmap=cmaps[2], norm=norm)
plot_label('Hypocentral Distance (km)', 'Travel Time (sec)', titles[1])
cax = plt.axes(cax_rects[1])
plt.colorbar(mappable=im1, cax=cax, orientation='horizontal')
cax.set_ylabel('P', fontsize=fsize_label)
cax = plt.axes(cax_rects[2])
plt.colorbar(mappable=im2, cax=cax, orientation='horizontal')
cax.set_ylabel('S', fontsize=fsize_label)
plt.tight_layout()
plt.savefig(fout)
