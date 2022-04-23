""" Plot b-value mapping
"""
import os, sys
sys.path.append('/home/zhouyj/software/data_prep')
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime
from reader import read_fctlg_np, read_fault, slice_ctlg, slice_ctlg_circle
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlg = 'input/fctlg_eg1.csv'
ffault = 'input/faults_eg.dat'
fout = 'output/eg_b-map.pdf'
titles = ['(a) b-Value', '(b) b-Uncertainty', '(c) Mc']
# slicing criteria
ot_rng = '20190704-20190710'
ot_rng = [UTCDateTime(date) for date in ot_rng.split('-')]
lon_rng =  [-117.82, -117.27]
lat_rng = [35.45, 36.05]
dep_rng = [0, 15]
mag_rng = [-1,8]
# b-value calc params
xy_grid = 0.04
slice_rad = 0.04
min_num = 200
b_rng = [0.3,1.] # if instable b estimation
# fig config
fig_size = (16, 8)
fsize_label = 14
fsize_title = 18
mag_corr = 0.5
marker_size = 3.
cmap = plt.get_cmap('coolwarm')
alpha = 0.4
cbar_frac = 0.035 # size
cbar_asp = 15 # shape
cbar_pad = 0.06 # loc
line_wid = 1. # fault trace

# read catalog
events = read_fctlg_np(fctlg)
events = slice_ctlg(events, ot_rng=ot_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng)
faults = read_fault(ffault, lat_rng, lon_rng)

# calc b map
def calc_fmd(mag):
    mag = mag[mag!=-np.inf]
    mag_max = np.ceil(10 * max(mag)) / 10
    mag_min = np.floor(10 * min(mag)) / 10
    mag_bin = np.around(np.arange(mag_min-0.1, mag_max+0.2, 0.1),1)
    num = np.histogram(mag, mag_bin)[0]
    cum_num = np.cumsum(num[::-1])[::-1]
    return mag_bin[1:], num, cum_num

def calc_mc_maxc(mag):
    mag_bin, num, _ = calc_fmd(mag)
    return mag_bin[np.argmax(num)]

def calc_b(mag, min_num=None):
    num_events = len(mag)
    if min_num: 
        if num_events < min_num: return -1, -1
    b_val = np.log10(np.exp(1)) / (np.mean(mag) - np.min(mag) + 0.05)
    b_dev = 2.3 * b_val**2 * (np.var(mag) / num_events)**0.5
    return round(b_val,2), round(b_dev,2)

def gr_fit(mag, min_num=100):
    if len(mag) < min_num: return np.nan, [np.nan, np.nan], np.nan
    mag = np.array(mag)
    mc = calc_mc_maxc(mag) # MAXC method
    mag = mag[mag>=mc]
    b_val, b_dev = calc_b(mag)
    return mc, [b_val, b_dev], np.log10(len(mag))

def slice_calc_mc_b(events, lat_i, lon_j):
    events_i = slice_ctlg_circle(events, lat_i, lon_j, slice_rad)
    if len(events_i)<min_num: return np.nan, np.nan, np.nan, np.nan
    mag = events_i['mag']
    mc, [b_val, b_dev], a_val = gr_fit(events_i['mag'], min_num=min_num)
    return mc, b_val, b_dev, a_val

lat = np.arange(lat_rng[0], lat_rng[1], xy_grid)
lon = np.arange(lon_rng[0], lon_rng[1], xy_grid)
b_mat = -np.ones([len(lat), len(lon)])
b_dev_mat = -np.ones([len(lat), len(lon)])
a_mat = -np.ones([len(lat), len(lon)])
mc_mat = -np.ones([len(lat), len(lon)])
cos_lat = np.cos(np.mean(lat)*np.pi/180)
for i,lat_i in enumerate(lat):
  for j,lon_j in enumerate(lon):
    mc_mat[i,j], b_mat[i,j], b_dev_mat[i,j], a_mat[i,j] = slice_calc_mc_b(events, lat_i, lon_j)

# drop bad b
cond_b = (b_rng[0]>b_mat) + (b_rng[1]<b_mat)
b_mat[cond_b] = np.nan
mc_mat[cond_b] = np.nan
a_mat[cond_b] = np.nan
b_dev_mat[cond_b] = np.nan

def plot_label(xlabel=None, ylabel=None, title=None, yvis=True):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label, visible=yvis)

def plot_map(d_mat):
    ax = plt.gca()
    im = plt.imshow(d_mat, cmap=cmap, origin='lower', 
                    extent=[lon[0]-xy_grid/2, lon[-1]+xy_grid/2,
                            lat[0]-xy_grid/2, lat[-1]+xy_grid/2])
    cbar = plt.colorbar(im, ax=ax, fraction=cbar_frac, aspect=cbar_asp, pad=cbar_pad, orientation='horizontal')
    # plot faults and events
    for fault in faults:
        plt.plot(fault[:,0], fault[:,1], color='k', linewidth=line_wid)
    mag = (np.array(list(events['mag'])) + mag_corr) * marker_size
    plt.scatter(events['lon'], events['lat'], mag, color='gray', edgecolor='none', alpha=alpha, zorder=len(faults)+3)
    ax.set_aspect(1/cos_lat)
    plt.setp(cbar.ax.xaxis.get_majorticklabels(), fontsize=fsize_label)

fig = plt.figure(figsize=fig_size)
plt.subplot(1,3,1)
plot_map(b_mat)
plot_label(title=titles[0])
plt.annotate('$R_{slice} = %s\degree$\n$N_{min} = %s$'%(slice_rad, min_num), (lon_rng[0],lat_rng[0]), fontsize=fsize_label)
plt.subplot(1,3,2)
plot_map(b_dev_mat)
plot_label(title=titles[1], yvis=False)
plt.subplot(1,3,3)
plot_map(mc_mat)
plot_label(title=titles[2], yvis=False)
# save fig
plt.tight_layout()
plt.savefig(fout)
