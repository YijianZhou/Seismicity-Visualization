""" Plot b mapping
"""
import os
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
print('lat range:', lat[0],lat[-1])
print('lon range:', lon[0],lon[-1])
b_mat = -np.ones([len(lat), len(lon)])
mc_mat = -np.ones([len(lat), len(lon)])
slice_radius = cfg.slice_radius
min_num = cfg.min_num
max_b = cfg.max_b
min_mc = cfg.min_mc
num_proc = cfg.num_proc
# plot config
fig_root, fig_fname = os.path.split(cfg.fig_fname)
fig_title = cfg.fig_title
fig_size = cfg.fig_size
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mag_corr = cfg.mag_corr
mark_size = cfg.mark_size
cmap = plt.get_cmap(cfg.cmap)
alpha = cfg.alpha
cbar_frac = cfg.cbar_frac
cbar_asp = cfg.cbar_asp
line_wid = cfg.line_wid
# read & filter catalog
events = read_ctlg(ctlg_path)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng)
mag = (np.array(list(events['mag'])) + mag_corr) * mark_size
faults = read_fault(fault_path, lat_rng, lon_rng)

def slice_calc_mc_b(lati, loni):
    eventsi = slice_ctlg_circle(events, lati, loni, slice_radius)
    mc, [b_val, b_dev] = calc_mc_b(eventsi['mag'], min_num=min_num)
    return mc, b_val

# calc mc & b map
if num_proc==1:
    for i,lati in enumerate(lat):
      for j,loni in enumerate(lon):
        mc_mat[i,j], b_mat[i,j] = slice_calc_mc_b(lati, loni)
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
        mc_mat[i,j], b_mat[i,j] = outi[2:].get()
# drop bad b
cond_b = b_mat>max_b
cond_mc = mc_mat<min_mc
b_mat[cond_b+cond_mc] = np.nan
mc_mat[cond_b+cond_mc] = np.nan

# plot b mapping
fig = plt.figure(figsize=fig_size)
ax = plt.gca()
im = plt.imshow(b_mat, cmap=cmap, origin='lower', 
                extent=[lon[0]-xy_grid/2, lon[-1]+xy_grid/2,
                        lat[0]-xy_grid/2, lat[-1]+xy_grid/2])
cbar = plt.colorbar(im, ax=ax, fraction=cbar_frac, aspect=cbar_asp)
# plot faults and events
for fault in faults: plt.plot(fault[:,0], fault[:,1], color='k', linewidth=line_wid)
plt.scatter(events['lon'], events['lat'], mag, color='gray', alpha=alpha)
# tune fig
cbar.ax.set_ylabel('b-value', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title('b-Value Map: %s'%fig_title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig('%s/b_%s'%(fig_root, fig_fname))

# plot b mapping
fig = plt.figure(figsize=fig_size)
ax = plt.gca()
im = plt.imshow(mc_mat, cmap=cmap, origin='lower',
                extent=[lon[0]-xy_grid/2, lon[-1]+xy_grid/2,
                        lat[0]-xy_grid/2, lat[-1]+xy_grid/2])
cbar = plt.colorbar(im, ax=ax, fraction=cbar_frac, aspect=cbar_asp)
# plot faults and events
for fault in faults: plt.plot(fault[:,0], fault[:,1], color='k', linewidth=line_wid)
plt.scatter(events['lon'], events['lat'], mag, color='gray', alpha=alpha)
# tune fig
cbar.ax.set_ylabel('Mc', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title('Mc Map: %s'%fig_title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig('%s/mc_%s'%(fig_root, fig_fname))
plt.show()
