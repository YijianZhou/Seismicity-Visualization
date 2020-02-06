""" Plot earthquake location
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import config
from reader import read_ctlg

# catalog info
cfg = config.Config_Loc()
ctlg_path = cfg.ctlg_path
lon_rng = cfg.lon_rng
lat_rng = cfg.lat_rng
dep_rng = cfg.dep_rng

# plot config
fig_title = cfg.fig_title
fig_fname = cfg.fig_fname
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mark_size = cfg.mark_size
fig_xsize = cfg.fig_xsize
fig_ysize = fig_xsize * (lat_rng[1]-lat_rng[0]) / (lon_rng[1]-lon_rng[0])
alpha = cfg.alpha
cmap = plt.get_cmap(cfg.cmap)
cbar_pos = cfg.cbar_pos
cbar_ticks = cfg.cbar_ticks

# read & filter
events = read_ctlg(ctlg_path)
lat_cond = (events['lat']>lat_rng[0])*(events['lat']<lat_rng[1])
lon_cond = (events['lon']>lon_rng[0])*(events['lon']<lon_rng[1])
dep_cond = (events['dep']>dep_rng[0])*(events['dep']<dep_rng[1])
events = events[lat_cond * lon_cond * dep_cond]
lat = list(events['lat'])
lon = list(events['lon'])
dep = list(events['dep'])
mag = list(events['mag'] * mark_size)

# 1. plot dep hist
plt.figure()
plt.hist(dep)
ax = plt.gca()
plt.xlabel('Depth (km)', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
# 2. plot loc
plt.style.use('ggplot')
fig = plt.figure(figsize=(fig_xsize, fig_ysize))
color = [cmap(1-di/dep_rng[1]) for di in dep]
plt.scatter(lon, lat, mag, alpha=alpha, color=color)
# fill up edge
edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]]
edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
plt.xlabel('Longitude', fontsize=fsize_label)
plt.ylabel('Latitude', fontsize=fsize_label)
plt.title(fig_title, fontsize=fsize_title)
# plot colorbar
cbar_ax = fig.add_axes(cbar_pos)
cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
cbar.set_label('Depth (km)')
cbar_tlabels = [str((1-tick)*dep_rng[1]) for tick in cbar_ticks]
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tlabels)
# save & show 
plt.savefig(fig_fname)
plt.show()
