""" Plot cross-section profile: multiple fault segments
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
title = 'Example Cross-Section View: Multiple Fault Segments'
fout = 'output/example_prof_multi-seg.pdf'
# catalog info
lon_rng = [100.5, 104]
lat_rng = [26.5, 30.7]
dep_rng = [0, 35]
mag_rng = [0., 6]
dep_corr = 0.
mag_corr = 1.
ref_pnts = np.array(\
   [[101.992,29.9833],
    [102.258,29.3083],
    [102.242,27.9750],
    [102.800,26.9583]])
pnt_names = ["A","B","C","D"]
num_seg = len(pnt_names) - 1
prof_wid = 4 # km
# fig params
fig_size = (16*0.8,6*0.8)
mark_size = 5.
alpha=0.8
color = 'tab:blue'
fsize_label = 14
fsize_title = 18
xlabel = 'Along-Strike Distance (km)'
ylabel = 'Depth (km)'

# read & filter
events = read_ctlg(fctlg)
events = slice_ctlg(events, lat_rng=lat_rng, lon_rng=lon_rng, dep_rng=dep_rng, mag_rng=mag_rng)
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
    return np.array(prof_dist), np.array(prof_dep), np.array(prof_mag), abs_ab*111


# start plot
plt.figure(figsize=fig_size)
ax = plt.gca()
ax.invert_yaxis()
done_dist = 0
for i in range(num_seg):
    # proj to proile
    prof_dist, prof_dep, prof_mag, abs_ab = calc_prof(ref_pnts[i:i+2])
    prof_dist += done_dist
    abs_ab += done_dist
    plt.scatter(prof_dist, prof_dep, prof_mag, color=color, edgecolor='none', alpha=alpha)
    # plot ref pnt
    if i==0: plt.annotate(pnt_names[0], (done_dist,dep_rng[0]), fontsize=fsize_label, va='top', ha='center')
    plt.annotate(pnt_names[i+1], (abs_ab,dep_rng[0]), fontsize=fsize_label, va='top', ha='center')
    # fill edge
    edgex = [done_dist,done_dist,abs_ab,abs_ab]
    edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
    plt.scatter(edgex, edgey, alpha=0)
    # next seg
    done_dist = abs_ab

# fill edge
edgex = [0,0,abs_ab,abs_ab]
edgey = [dep_rng[0],dep_rng[1],dep_rng[0],dep_rng[1]]
plt.scatter(edgex, edgey, alpha=0)
# annote params
plt.annotate('Profile Width = $\pm$%skm \n$M_{C} = %s$'%(prof_wid, mag_rng[0]), (0,dep_rng[1]), fontsize=fsize_label)
# plot label
plt.xlabel(xlabel, fontsize=fsize_label)
plt.ylabel(ylabel, fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
plt.tight_layout()
plt.savefig(fout)
plt.show()
