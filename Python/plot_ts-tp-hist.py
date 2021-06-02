""" Histogram of ts-tp 
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np

# i/o paths
fpha = 'input/example.pha'
fout = 'output/example_ts-tp-hist.pdf'
# fig config
fig_size = (8,6)
fsize_label = 14
fsize_title = 18
bins = np.arange(0,15.1,1.)

# read fpha
ts_tp = []
f=open(fpha); lines=f.readlines(); f.close()
for line in lines:
    codes = line.split(',')
    if len(codes[0])>10: continue
    tp, ts = [UTCDateTime(code) for code in codes[1:3]]
    ti = ts - tp
    if 0<ti<15: ts_tp.append(ti)

plt.figure(figsize=fig_size)
ax = plt.gca()
plt.hist(ts_tp, bins=bins, edgecolor='tab:gray', alpha=0.8)
plt.xlabel('ts - tp (sec)', fontsize=fsize_label)
plt.ylabel('Number of Picks', fontsize=fsize_label)
plt.title('ts-tp Histogram', fontsize=fsize_title)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.tight_layout()
plt.savefig(fout)
