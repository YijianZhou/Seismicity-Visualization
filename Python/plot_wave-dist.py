""" Plot waveform with x-y as travel time and epicentral distance
"""
import os, glob, sys
sys.path.append('/home/zhouyj/software/data_prep')
from obspy import read, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
from signal_lib import preprocess, calc_dist_km
from reader import dtime2str, get_data_dict
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fsta = 'input/station_eg.csv'
data_root = '/data/Example_data'
get_data_dict = get_data_dict
get_sta_dict = dp.get_sta_dict
sta_dict = get_sta_dict(fsta)
# event info
ot, lat, lon, dep, mag = '2019-07-07T08:08:48.100000Z', 35.855, -117.6692, 5, 3
ot = UTCDateTime(ot)
event_name = dtime2str(ot)
data_dict = get_data_dict(ot, data_root)
fout = 'output/eg_wave-dist_%s.pdf'%event_name
# data preprocess
freq_band = [1,40]
samp_rate = 100
win_len = 60
win_len_npts = int(win_len * samp_rate)
time = np.arange(win_len_npts) / samp_rate
max_dist = 200
chn_idx = 2 # E,N,Z
amp = 2
# fig config
fig_size = (12,14)
fsize_label = 14
fsize_title = 18
title = 'Example Waveform Moveout: %s M%s'%(event_name, mag)
line_wid = 1
alpha = 0.8
colors = ['tab:'+color for color in ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']]

# read data
dtype = [('sta','O'),('data','O'),('dist','O')]
sta_data = []
for net_sta, sta_loc in sta_dict.items():
    if net_sta not in data_dict: continue
    st_path = data_dict[net_sta][chn_idx]
    st = read(st_path, starttime=ot, endtime=ot+win_len)
    if len(st)==0: continue
    st = preprocess(st, samp_rate, freq_band).normalize()
    if len(st)==0: continue
    print('read %s'%st_path)
    dist = calc_dist_km([lat,sta_loc['sta_lat']],[lon,sta_loc['sta_lon']])
    if dist>max_dist: continue
    sta_data.append((net_sta, st[0].data[0:win_len_npts]*amp + dist, dist))
sta_data = np.array(sta_data, dtype=dtype)
sta_data = np.sort(sta_data, order='dist')

# start plot
plt.figure(figsize=fig_size)
ax = plt.gca()
for i, [net_sta, data, _] in enumerate(sta_data):
    plt.plot(time, data, linewidth=line_wid, color=colors[i%10], alpha=alpha)
    plt.annotate(net_sta, (time[0],data[0]), fontsize=fsize_label, ha='left', va='bottom')
plt.xlabel('Travel Time (sec)', fontsize=fsize_label)
plt.ylabel('Epicentral Distance (km)', fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.tight_layout()
plt.savefig(fout)
