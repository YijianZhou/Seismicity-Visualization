""" Plot earthquake location
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import config
from reader import read_ctlg, slice_ctlg, read_fault

# catalog info
cfg = config.Config_Loc()
ctlg_path = cfg.ctlg_path
lon_rng = cfg.lon_rng
lat_rng = cfg.lat_rng
dep_rng = cfg.dep_rng
x_ratio = np.cos(lat_rng[0] * np.pi / 180)
prof_pnt = cfg.prof_pnt
prof_wd = cfg.prof_wd / 111 # km to deg
# plot config
fig_title = cfg.fig_title
fig_fname = cfg.fig_fname
prof_name = cfg.prof_name
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mag_corr = cfg.mag_corr
mark_size = cfg.mark_size
fig_xsize = cfg.fig_xsize
fig_ysize = fig_xsize * (lat_rng[1]-lat_rng[0]) / (lon_rng[1]-lon_rng[0])
alpha = cfg.alpha
cmap = plt.get_cmap(cfg.cmap)
cbar_pos = cfg.cbar_pos
cbar_ticks = cfg.cbar_ticks
plot_prof = cfg.plot_prof
line_wid = cfg.line_wid

# read & filter
events = read_ctlg(ctlg_path)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
num_events = len(events)
lat = np.array(list(events['lat']))
lon = np.array(list(events['lon']))
dep = np.array(list(events['dep']))
mag = (np.array(list(events['mag'])) + mag_corr) * mark_size
faults = read_fault(cfg.fault_path, lat_rng, lon_rng)

# calc along profile dist
prof_dist, prof_dep, prof_mag = [], [], []
vec_ab = prof_pnt[1] - prof_pnt[0]
vec_ab[0] *= x_ratio
abs_ab = np.linalg.norm(vec_ab)
for i in range(num_events):
    loc_c = np.array([lon[i], lat[i]])
    vec_ac = loc_c - prof_pnt[0]
    vec_ac[0] *= x_ratio
    abs_ac = np.linalg.norm(vec_ac)
    cos = vec_ac.dot(vec_ab) / abs_ab / abs_ac
    if abs_ac * (1-cos**2)**0.5 > prof_wd: continue
    if cos<0 or abs_ac*cos>abs_ab: continue
    prof_dist.append(abs_ac * cos * 111)
    prof_dep.append(dep[i])
    prof_mag.append(mag[i])

# 1. plot dep hist
plt.figure()
ax = plt.gca()
plt.hist(dep)
plt.xlabel('Depth (km)', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
plt.tight_layout()

# 2. plot profile
plt.figure(figsize=(abs_ab*20,8))
ax = plt.gca()
ax.invert_yaxis()
edgex = [0,0,abs_ab*111,abs_ab*111]
edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
plt.scatter(prof_dist, prof_dep, prof_mag, alpha=alpha)
plt.scatter(edgex, edgey, alpha=0)
plt.annotate('A', (0, 0))
plt.annotate('B', (abs_ab*111, 0))
plt.xlabel('Along-Profile Distance (km)', fontsize=fsize_label)
plt.ylabel('Depth (km)', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig(prof_name)

# 3. plot map view
plt.style.use('ggplot')
fig = plt.figure(figsize=(fig_xsize, fig_ysize))
ax = plt.gca()
color = [cmap(1-di/dep_rng[1]) for di in dep]
# events & reference  profile points
if plot_prof:
    plt.plot(prof_pnt[:,0], prof_pnt[:,1], 'w--')
    plt.annotate('A', (prof_pnt[0,0], prof_pnt[0,1]))
    plt.annotate('B', (prof_pnt[1,0], prof_pnt[1,1]))
plt.scatter(lon, lat, mag, alpha=alpha, color=color, zorder=len(faults)+1)
# plot fault
for fault in faults: plt.plot(fault[:,0], fault[:,1], color='gray', linewidth=line_wid)
# fill up edge
edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]]
edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
plt.xlabel('Longitude', fontsize=fsize_label)
plt.ylabel('Latitude', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
# plot colorbar
cbar_ax = fig.add_axes(cbar_pos)
cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
cbar.set_label('Depth (km)', rotation=-90, va="bottom")
cbar_tlabels = [str((1-tick)*dep_rng[1]) for tick in cbar_ticks]
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tlabels)
plt.tight_layout()
plt.savefig(fig_fname)
plt.show()
