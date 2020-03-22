""" Plot b mapping
"""
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from obspy import UTCDateTime
from reader import read_pad_det, read_ctlg, read_fault, slice_ctlg, slice_ctlg_circle
from statis_lib import calc_mc_b
import config

# catalog info
cfg = config.Config_b_Map()
ctlg_path = cfg.ctlg_path
fault_path = cfg.fault_path
lat_rng = cfg.lat_rng
lon_rng = cfg.lon_rng
# calc params
xy_grid = cfg.xy_grid
lat = np.arange(lat_rng[0], lat_rng[1], xy_grid)
lon = np.arange(lon_rng[0], lon_rng[1], xy_grid)
print(lat)
print(lon)
b_mat = -np.ones([len(lat), len(lon)])
slice_radius = cfg.slice_radius
min_num = cfg.min_num
num_proc = cfg.num_proc
# plot config
fig_fname = cfg.fig_fname
fig_title = cfg.fig_title
fig_size = cfg.fig_size
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mag_corr = cfg.mag_corr
mark_size = cfg.mark_size
cmap = plt.get_cmap(cfg.cmap)
alpha = cfg.alpha
# read & filter catalog
events = read_ctlg(ctlg_path)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng)
mag = (np.array(list(events['mag'])) + mag_corr) * mark_size
faults = read_fault(fault_path, lat_rng, lon_rng)

def calc_b(lati, loni):
    eventsi = slice_ctlg_circle(events, lati, loni, slice_radius)
    mc, [b_val, b_dev] = calc_mc_b(eventsi['mag'], min_num=min_num)
    return b_val

# calc b map
if num_proc==1:
    for i,lati in enumerate(lat):
      for j,loni in enumerate(lon):
        b_mat[i,j] = calc_b(lati, loni)
else:
    pool = mp.Pool(num_proc)
    out=[]
    for i,lati in enumerate(lat):
      for j,loni in enumerate(lon):
        out.append([i,j,pool.apply_async(calc_b, args=(lati, loni,))])
    pool.close()
    pool.join()
    for outi in out:
        i, j = outi[0:2]
        b_mat[i,j] = outi[-1].get()

# plot b mapping
fig = plt.figure(figsize=fig_size)
ax = plt.gca()
im = plt.imshow(b_mat, cmap=cmap, origin='lower', 
                extent=[lon[0]-xy_grid/2, lon[-1]+xy_grid/2,
                        lat[0]-xy_grid/2, lat[-1]+xy_grid/2])
cbar = plt.colorbar(im, ax=ax, fraction=0.05)
# plot faults and events
for fault in faults: plt.plot(fault[:,0], fault[:,1], color='k', linewidth=1)
plt.scatter(events['lon'], events['lat'], mag, color='gray', alpha=alpha)
# tune fig
cbar.ax.set_ylabel('b-value', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig(fig_fname)
plt.show()
