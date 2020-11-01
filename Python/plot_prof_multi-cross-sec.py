""" Plot cross-section profile: Multiple cross-sections
"""
import sys
sys.path.append('/home/zhouyj/software/seis_view')
import numpy as np
import matplotlib.pyplot as plt
from reader import read_ctlg, slice_ctlg
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlg = 'input/catalog_example.csv'
title = 'Example Cross-Section View: Multiple Cross-Sections'
fout = 'output/example_prof_multi-cross-sec.pdf'
# catalog info
lon_rng = [102.23, 102.32]
lat_rng = [29.14, 29.25]
dep_rng = [5, 15]
dep_corr = 0
mag_corr = 1.
ref_pnts = np.array(\
  [[102.26,29.235],[102.285,29.165],
   [102.25,29.2],[102.29,29.21],
   [102.255,29.18],[102.295,29.19]]) # [lon,lat]
pnt_names = ["A","A'","B","B'","C","C'"]
prof_wids = [1.5,1,1] # km
# fig params
fig_size = (10*0.8, 10*0.8)
subplots = [212,221,222]
mark_size = 5.
alpha=0.8
color = 'tab:blue'
fsize_label = 12
fsize_title = 14
xlabel = 'Along-Profile Distance (km)'
ylabel = 'Depth (km)'
subplot_rect = {'left':0.08, 'right':0.96, 'bottom':0.08, 'top':0.95, 'wspace':0.1, 'hspace':0.1}

# read catalog
events = read_ctlg(fctlg)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
lat = np.array(list(events['lat']))
lon = np.array(list(events['lon']))
dep = np.array(list(events['dep'])) + dep_corr
mag = (np.array(list(events['mag'])) + mag_corr) * mark_size
num_events = len(events)

# calc along profile dist
def calc_prof(ref_pnt):
    prof_dist, prof_dep, prof_mag = [], [], []
    cos_lat = np.cos(ref_pnt[0][1]*np.pi/180)
    vec_ab = ref_pnt[1] - ref_pnt[0]
    vec_ab[0] *= cos_lat
    abs_ab = np.linalg.norm(vec_ab)
    for i in range(num_events):
        loc_c = np.array([lon[i], lat[i]])
        vec_ac = loc_c - ref_pnt[0]
        vec_ac[0] *= cos_lat
        abs_ac = np.linalg.norm(vec_ac)
        cos = vec_ac.dot(vec_ab) / abs_ab / abs_ac
        if abs_ac * (1-cos**2)**0.5 > prof_wid/111.: continue
        if cos<0 or abs_ac*cos>abs_ab: continue
        prof_dist.append(abs_ac * cos * 111)
        prof_dep.append(dep[i])
        prof_mag.append(mag[i])
    return prof_dist, prof_dep, prof_mag, abs_ab*111

def plot_label(xlabel=None, ylabel=None, yvisible=True):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label, visible=yvisible)


# start plot
plt.figure(figsize=fig_size)
for i,subplot in enumerate(subplots):
    # get specific params
    prof_wid = prof_wids[i]
    # plot subplot
    plt.subplot(subplot)
    ax = plt.gca()
    ax.invert_yaxis()
    # proj to proile
    prof_dist, prof_dep, prof_mag, abs_ab = calc_prof(ref_pnts[2*i:2*i+2])
    plt.scatter(prof_dist, prof_dep, prof_mag, color=color, edgecolor='none', alpha=alpha)
    # plot ref pnt
    plt.annotate(pnt_names[2*i], (0,dep_rng[0]), fontsize=fsize_label, va='top', ha='center')
    plt.annotate(pnt_names[2*i+1], (abs_ab,dep_rng[0]), fontsize=fsize_label, va='top', ha='center')
    # fill edge
    edgex = [0,0,abs_ab,abs_ab]
    edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
    plt.scatter(edgex, edgey, alpha=0)
    if i==0: plot_label(xlabel,ylabel)
    elif i==1: plot_label(ylabel=ylabel)
    else: plot_label(yvisible=False)
plt.suptitle(title, fontsize=fsize_title)
plt.subplots_adjust(**subplot_rect)
plt.savefig(fout)
plt.show()
