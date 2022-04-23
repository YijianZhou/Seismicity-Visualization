""" Plot earthquake location map & cross-sections
"""
import sys
sys.path.append('/home/zhouyj/software/seis_view')
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from reader import read_ctlg, slice_ctlg
import warnings
warnings.filterwarnings("ignore")

# 1. catalog info
fctlg = 'input/example.ctlg'
fig_title = 'Example Plot of Loc Map & Cross-sections'
fout = 'output/example_loc_prof.pdf'
lon_rng = [104.68,105.]
lat_rng = [28.28,28.52]
dep_rng = [0, 15]
mag_corr = 1.
dep_corr = 0

# 2. fig layout
fig_size = (16*0.8, 14*0.8)
num_sub = 6
subplot_grids = [(4,4)]*2 + [(num_sub,4)]*num_sub
org_grids = [(0,0),(3,0)] + [(i,3) for i in range(num_sub)]
col_spans = [3,3] + [1]*num_sub
row_spans = [3,1] + [1]*num_sub
subplot_rect = {'left':0.08, 'right':0.94, 'bottom':0.06, 'top':0.96, 'wspace':0.1, 'hspace':0.15}
# event points
alpha = 0.6
cmap = plt.get_cmap('hot')
plt_style = ['ggplot',None][1]
mark_size = 2.
bg_color = 'darkgray'
grid_color = 'lightgray'
# color bar
cbar_pos = [0.62,0.72,0.02,0.18] # pos in ax: left
cbar_ticks = np.arange(0,1.,0.333)
cbar_tlabels = ['15','10','5','0']
# ref points
ref_pnt_size = 10
# text
fsize_label = 14
fsize_title = 18

# 3. reference points of cross-sections
def polar2xy(prof_polar):
    prof_xy = []
    for [lon0, lat0, theta] in prof_polar:
        lon1 = lon0 - np.cos(theta*np.pi/180) * prof_len/2
        lon2 = lon0 + np.cos(theta*np.pi/180) * prof_len/2
        lat1 = lat0 - np.sin(theta*np.pi/180) * prof_len/2
        lat2 = lat0 + np.sin(theta*np.pi/180) * prof_len/2
        prof_xy += [[lon1,lat1],[lon2,lat2]]
    return np.array(prof_xy)

# main prof
main_pnt = np.array([[104.7,28.45],[104.97,28.35]])
main_wid = 5/111 # degree
main_names = ["O","O'"]
rect_main_color = 'tab:blue'
# sub prof
sub_theta = abs(np.arctan((main_pnt[0,0]-main_pnt[1,0])/(main_pnt[0,1]-main_pnt[1,1]))) * 180/np.pi
lon_step = (main_pnt[1][0] - main_pnt[0][0])/num_sub
lat_step = (main_pnt[1][1] - main_pnt[0][1])/num_sub
prof_pnts_polar = np.array([\
    [main_pnt[0][0]+(i+0.5)*lon_step,
     main_pnt[0][1]+(i+0.5)*lat_step, sub_theta] for i in range(num_sub)])
prof_len = 12/111 # degree
cos_lat = np.cos(main_pnt[0][1]*np.pi/180)
prof_wid = ((lon_step*cos_lat)**2 + lat_step**2)**0.5 /2 # degree
pnt_names = ["A","A'","B","B'","C","C'","D","D'","E","E'","F","F'"]
prof_pnts = polar2xy(prof_pnts_polar)
rect_sub_color = 'tab:green'


# read catalog
events = read_ctlg(fctlg)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng)
num_events = len(events)
lat = np.array(list(events['lat']))
lon = np.array(list(events['lon']))
dep = np.array(list(events['dep'])) + dep_corr
mag = (np.array(list(events['mag'])) + mag_corr) * mark_size


""" cross-section functions
"""

def calc_dist(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return (dx**2 + dy**2)**0.5


# calc along profile dist
def calc_prof(ref_pnt, prof_wid):
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
        if abs_ac * (1-cos**2)**0.5 > prof_wid: continue
        if cos<0 or abs_ac*cos>abs_ab: continue
        prof_dist.append(abs_ac * cos * 111)
        prof_dep.append(dep[i])
        prof_mag.append(mag[i])
    return prof_dist, prof_dep, prof_mag, abs_ab*111


def plot_rect(prof_pnts, prof_wid, color):
    num_profs = int(len(prof_pnts)/2)
    for j in range(num_profs):
        refs = prof_pnts[j*2:j*2+2]
        theta = np.arctan((refs[1][1]-refs[0][1]) / (refs[1][0]-refs[0][0]))
        W = prof_wid * ((cos_lat*np.sin(theta))**2 + np.cos(theta)**2)**-0.5
        L = calc_dist(refs[0], refs[1])
        x0, y0 = np.mean(refs[:,0]), np.mean(refs[:,1])
        theta = np.rad2deg(theta)
        tr = mpl.transforms.Affine2D().rotate_deg_around(x0, y0, theta) + tr0
        rect = pat.Rectangle((x0-L/2, y0-W),L,2*W, linewidth=1.5, ls='--', edgecolor=color, facecolor='none', transform=tr)
        ax.add_patch(rect)
    return 


def plot_prof(color):
    edgex = [0,0,abs_ab,abs_ab]
    edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
    plt.scatter(prof_dist, prof_dep, prof_mag, color=color, edgecolor='none', alpha=alpha)
    plt.scatter(edgex, edgey, alpha=0)
    plt.annotate(prof_name[0], (0, 0), fontsize=fsize_label, ha='center', va='top')
    plt.annotate(prof_name[1], (abs_ab, 0), fontsize=fsize_label, ha='center', va='top')
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)


def plot_label(xlabel=None, ylabel=None, yvisible=True):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label, visible=yvisible)


# start plotting
if plt_style: plt.style.use(plt_style)
fig = plt.figure(figsize=fig_size)
# 1. plot map view
ax = plt.subplot2grid(subplot_grids[0], org_grids[0], colspan=col_spans[0], rowspan=row_spans[0])
ax.set_facecolor(bg_color)
tr0 = ax.transData
# 1.1 seismic events
# fill up edge
edgex = [lon_rng[0], lon_rng[0], lon_rng[1], lon_rng[1]]
edgey = [lat_rng[0], lat_rng[1], lat_rng[0], lat_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
# plot seis events
color = [cmap(1-(di-dep_rng[0])/(dep_rng[1]-dep_rng[0])) for di in dep]
plt.scatter(lon, lat, mag, alpha=alpha, color=color, zorder=2)
plt.grid(True, color=grid_color)
# label & title
plt.title(fig_title, fontsize=fsize_title)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)

# 1.2 plot reference rectangles of cross-section
# sub profiles
num = len(prof_pnts)
for j in range(num):
    name = pnt_names[j]
    x, y = prof_pnts[j]
    va = 'top' if j%2==0 else 'bottom'
    plt.annotate(name, (x,y), fontsize=fsize_label, va=va, ha='center')
    plt.scatter([x],[y],[10], 'k')
plot_rect(prof_pnts, prof_wid, rect_sub_color)
# main profile
for j in range(2):
    name = main_names[j]
    x, y = main_pnt[j]
    ha = 'right' if j%2==0 else 'left'
    plt.annotate(name, (x,y), fontsize=fsize_label, va='center', ha=ha)
    plt.scatter([x],[y],[ref_pnt_size], 'k')
plot_rect(main_pnt, main_wid, rect_main_color)

# 1.3 plot colorbar
cbar_ax = fig.add_axes(cbar_pos)
cbar = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap)
cbar.set_label('Depth (km)', rotation=-90, va="bottom", fontsize=fsize_label)
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(cbar_tlabels)

# 2. plot cross-section
ax = plt.subplot2grid(subplot_grids[1], org_grids[1], colspan=col_spans[1], rowspan=row_spans[1])
prof_dist, prof_dep, prof_mag, abs_ab = calc_prof(main_pnt, main_wid)
prof_name = main_names
ax.invert_yaxis()
plot_prof(rect_main_color)
plt.xlabel('Along Profile Distance (km)', fontsize=fsize_label)
plt.ylabel('Depth (km)', fontsize=fsize_label)

# 3. plot sub profiles
num_prof = int(len(prof_pnts)/2)
for i in range(num_prof):
    ax = plt.subplot2grid(subplot_grids[2+i], org_grids[2+i], colspan=col_spans[2+i], rowspan=row_spans[2+i])
    prof_pnt = prof_pnts[i*2:i*2+2]
    prof_name = pnt_names[i*2:i*2+2]
    prof_dist, prof_dep, prof_mag, abs_ab = calc_prof(prof_pnt, prof_wid)
    ax.invert_yaxis()
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    plot_prof(rect_sub_color)
    plt.ylabel('Depth (km)', rotation=-90, va='bottom', fontsize=fsize_label)
    if i<num_prof-1: plt.setp(ax.xaxis.get_majorticklabels(), visible=False)
    if i==num_prof-1: plt.xlabel('Along Profile Distance (km)', fontsize=fsize_label)

# save fig
plt.subplots_adjust(**subplot_rect)
plt.savefig(fout)
plt.show()
