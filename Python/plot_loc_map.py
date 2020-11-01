""" Plot earthquake location in map view
"""
import sys
sys.path.append('/home/zhouyj/software/seis_view')
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from reader import read_ctlg, slice_ctlg
import warnings
warnings.filterwarnings("ignore")

# catalog info
fctlg = 'input/catalog_example.csv'
fig_title = 'Example Map Location Plot'
fout = 'output/example_loc_map.pdf'
lon_rng = [102.2, 102.35]
lat_rng = [29.125, 29.275]
dep_rng = [5, 15]
mag_corr = 1.
dep_corr = 0
# fig layout
fig_size = (10*0.8, 12*0.8)
# event points
alpha = 0.6
cmap = plt.get_cmap('hot')
plt_style = ['ggplot',None][1]
mark_size = 5.
bg_color = 'darkgray'
grid_color = 'lightgray'
# color bar
cbar_pos = [0.8,0.65,0.03,0.25] # pos in ax: left
cbar_ticks = np.arange(0,1.1,0.2)
cbar_tlabels = ['15','13','11','9','7','5']
# text
fsize_label = 12
fsize_title = 16

# read & filter
def read_catalog(fctlg):
    events = read_ctlg(fctlg)
    events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    lat = np.array(list(events['lat']))
    lon = np.array(list(events['lon']))
    dep = np.array(list(events['dep'])) + dep_corr
    mag = (np.array(list(events['mag'])) + mag_corr) * mark_size
    return lat, lon, dep, mag

# plot seis loc map
if plt_style: plt.style.use(plt_style)
fig = plt.figure(figsize=fig_size)
ax = plt.gca()
ax.set_facecolor(bg_color)
# fill up edge
edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]]
edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
# plot seis events
lat, lon, dep, mag = read_catalog(fctlg)
color = [cmap(1-(di-dep_rng[0])/(dep_rng[1]-dep_rng[0])) for di in dep]
plt.scatter(lon, lat, mag, alpha=alpha, color=color)
plt.grid(True, color=grid_color)
# label & title
plt.title(fig_title, fontsize=fsize_title)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
# plot colorbar
cbar_ax = fig.add_axes(cbar_pos)
cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
cbar.set_label('Depth (km)', rotation=-90, va="bottom", fontsize=fsize_label)
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tlabels)
# save fig
plt.tight_layout()
#plt.savefig(fout)
plt.show()
