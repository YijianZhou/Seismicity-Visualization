""" Plot data continuity
"""
import os, glob
import matplotlib.pyplot as plt
from obspy.core import read, UTCDateTime
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# i/o paths
stream_paths = '/data1/Makushin_raw/*/*HZ*' 
streams = glob.glob(stream_paths)
title = 'Example Data Continuity Plot'
# fig params
fsize_label = 14
fsize_title = 18
mark_size = 100

# stats for stations
sta_dict = {}
print('making station dict')
for stream in streams:
    st_dir, fname = os.path.split(stream)
    date = UTCDateTime(st_dir.split('/')[-1])
    net_sta = '.'.join(fname.split('.')[0:2])
    if net_sta not in sta_dict:
       sta_dict[net_sta] = [date.date]
    else:
       sta_dict[net_sta].append(date.date)

# plot continuity
print('plot continuity')
sta_dict_keys = sorted(list(sta_dict.keys()))
for i, sta_key in enumerate(sta_dict_keys):
    x1 = sta_dict[sta_key]
    plt.scatter(x1, [i]*len(x1), marker='s', s=mark_size)

ax = plt.gca()
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=20)
plt.yticks(list(range(len(sta_dict))), sta_dict_keys, fontsize=fsize_label)
plt.title(title, fontsize=fsize_title)
plt.grid(True)
plt.show()
