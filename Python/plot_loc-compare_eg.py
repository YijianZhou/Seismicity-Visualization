""" Plot location comparison in map view & cross-section
"""
import sys
sys.path.append('/home/zhouyj/software/data_prep')
import numpy as np
from obspy import UTCDateTime
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from reader import read_fctlg_np, slice_ctlg, read_fault
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fctlgs = ['input/fctlg_eg1.csv','input/fctlg_eg2.csv']
titles = ['(a) Catalog 1','(b) Catalog 2']
ffault = 'input/faults_eg.dat'
fout = 'output/eg_loc-compare.pdf'
num_ctlg = len(fctlgs)
# slicing criteria
ot_rng = '20190704-20190710'
ot_rng = [UTCDateTime(date) for date in ot_rng.split('-')]
lon_rng =  [-117.83, -117.28]
lat_rng = [35.47, 36.02]
dep_rng = [0, 15]
mag_rng = [-1,8]
mag_corr = .5 # avoid neg
cos_lat = np.cos(np.mean(lat_rng)*np.pi/180)
# fig config
fig_size = (14*0.8,11*0.8)
# subplot arrangement
subplot_grid = (5,4*num_ctlg)
org_grids = [(0,0),(0,4)] + [(4,0),(4,4)]
col_spans = [4]*2*num_ctlg
row_spans = [4]*num_ctlg + [1]*num_ctlg
# cross-sec config
main_pnt = np.array([[-117.75,35.94],[-117.34,35.54]])
main_wid = 8/111 # degree
main_name = ["O","O'"]
main_color = 'tab:blue'
ref_pnt_size = 10
# markers
line_wid = 1.
alpha = 0.6
cmap = plt.get_cmap('hot')
plt_style = ['ggplot',None][1]
marker_size = 1.
bg_color = 'darkgray'
grid_color = 'lightgray'
cbar_pos = [0.1,0.32,0.015,0.18] # vertical cbar, [x,y,dx,dy]
cbar_ticks = np.arange(0,1.1,0.333)
cbar_tlabels = ['15','10','5','0']
fsize_label = 14
fsize_title = 18

def read_catalog(fctlg):
    events = read_fctlg_np(fctlg)
    events['mag'] += mag_corr
    events = slice_ctlg(events, ot_rng=ot_rng, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
    print('%s | %s events'%(fctlg, len(events)))
    events = np.sort(events, order='ot')
    lat = np.array(list(events['lat']))
    lon = np.array(list(events['lon']))
    dep = np.array(list(events['dep']))
    mag = np.array(list(events['mag'])) * marker_size
    num_events = len(events)
    return lat, lon, dep, mag, num_events

def calc_dist(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return (dx**2 + dy**2)**0.5

def plot_rect(prof_pnts, prof_names, prof_wid, color):
    num_prof = int(len(prof_pnts)/2)
    for ii in range(num_prof):
        # ref rect
        prof_pnt = prof_pnts[ii*2:ii*2+2]
        W = prof_wid
        L = calc_dist(prof_pnt[0], prof_pnt[1])
        theta = np.rad2deg(np.arctan((prof_pnt[1][1]-prof_pnt[0][1]) / (prof_pnt[1][0]-prof_pnt[0][0])))
        x0, y0 = np.mean(prof_pnt[:,0]), np.mean(prof_pnt[:,1])
        tr = mpl.transforms.Affine2D().rotate_deg_around(x0, y0, theta) + tr0
        rect = pat.Rectangle((x0-L/2, y0-W),L,2*W, linewidth=1.5, ls='--', edgecolor=color, facecolor='none', transform=tr)
        ax.add_patch(rect)
        # ref point name
        for jj in range(2):
            name = prof_names[ii*2+jj]
            x, y = prof_pnt[jj]
            ha = 'right' if jj%2==0 else 'left'
            plt.annotate(name, (x,y), fontsize=fsize_label, va='center', ha=ha)
            plt.scatter([x],[y],[ref_pnt_size], 'k')

def calc_prof(prof_pnt, prof_wid):
    prof_dist, prof_dep, prof_mag = [], [], []
    vec_ab = prof_pnt[1] - prof_pnt[0]
    vec_ab[0] *= cos_lat
    abs_ab = np.linalg.norm(vec_ab)
    for i in range(num_events):
        loc_c = np.array([lon[i], lat[i]])
        vec_ac = loc_c - prof_pnt[0]
        vec_ac[0] *= cos_lat
        abs_ac = np.linalg.norm(vec_ac)
        cos = vec_ac.dot(vec_ab) / abs_ab / abs_ac
        if abs_ac * (1-cos**2)**0.5 > prof_wid: continue
        if cos<0 or abs_ac*cos>abs_ab: continue
        prof_dist.append(abs_ac * cos * 111)
        prof_dep.append(dep[i])
        prof_mag.append(mag[i])
    return prof_dist, prof_dep, prof_mag, abs_ab*111

def plot_prof(prof_name, color):
    edgex = [0,0,abs_ab,abs_ab]
    edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
    plt.scatter(prof_dist, prof_dep, prof_mag, color=color, edgecolor='none', alpha=alpha)
    plt.scatter(edgex, edgey, alpha=0)
    plt.annotate(prof_name[0], (0, 0), fontsize=fsize_label, ha='center', va='top')
    plt.annotate(prof_name[1], (abs_ab, 0), fontsize=fsize_label, ha='center', va='top')
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

def plot_label(xlabel=None, ylabel=None, title=None, yvis=True):
    ax = plt.gca()
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label, visible=yvis)

if plt_style: plt.style.use(plt_style)
fig = plt.figure(figsize=fig_size)
for i in range(num_ctlg):
  # 1. plot loc map
  ax = plt.subplot2grid(subplot_grid, org_grids[i], colspan=col_spans[i], rowspan=row_spans[i])
  ax.set_facecolor(bg_color)
  tr0 = ax.transData
  edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]] # fill up edge
  edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
  plt.scatter(edgex, edgey, alpha=0)
  # plot faults
  faults = read_fault(ffault, lat_rng, lon_rng)
  for fault in faults:
    plt.plot(fault[:,0], fault[:,1], color='gray', linewidth=line_wid, zorder=2)
  # plot seis events
  lat, lon, dep, mag, num_events = read_catalog(fctlgs[i])
  color = [cmap(1-(di-dep_rng[0])/(dep_rng[1]-dep_rng[0])) for di in dep]
  plt.scatter(lon, lat, mag, alpha=alpha, color=color, edgecolor='none', zorder=len(faults)+1)
  plt.grid(True, color=grid_color, zorder=1)
  plot_rect(main_pnt, main_name, main_wid, main_color)
  ax.set_aspect(1/cos_lat)
  yvis = True if i==0 else False
  plot_label(title=titles[i], yvis=yvis)
  if i==0:
    # plot colorbar
    cbar_ax = fig.add_axes(cbar_pos)
    cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
    cbar.set_label('Depth (km)', rotation=-90, va="bottom", fontsize=fsize_label)
    cbar.set_ticks(cbar_ticks)
    cbar.set_ticklabels(cbar_tlabels)
    plt.setp(cbar.ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
  # 2. plot cross-section
  ax = plt.subplot2grid(subplot_grid, org_grids[i+num_ctlg], colspan=col_spans[num_ctlg+i], rowspan=row_spans[num_ctlg+i])
  prof_dist, prof_dep, prof_mag, abs_ab = calc_prof(main_pnt, main_wid)
  ax.invert_yaxis()
  plot_prof(main_name, main_color)
  ax.set_aspect(1)
  ylabel = 'Depth (km)' if i==0 else None
  plot_label('Along Profile Distance (km)',ylabel,yvis=yvis)
# save fig
plt.tight_layout()
plt.savefig(fout)
