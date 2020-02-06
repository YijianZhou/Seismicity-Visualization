""" Plot FMD & M-t
"""
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime
from reader import read_ctlg
import config

# catalog info
cfg = config.Config_Mag()
ctlg_path = cfg.ctlg_path
mag_rng = cfg.mag_rng
# plot config
fig_title_fmd = cfg.fig_title_fmd
fig_title_mt = cfg.fig_title_mt
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mark_size = cfg.mark_size
alpha = cfg.alpha

# read & filter catalog
events = read_ctlg(ctlg_path)
mag_cond = (events['mag']>mag_rng[0])*(events['mag']<mag_rng[1])
events = events[mag_cond]
mag = list(events['mag'])
ot = [oti.datetime for oti in events['ot']]

# calc fmd
mag_min, mag_max = min(mag), max(mag)
print('mag rng:', mag_min, mag_max)
mag_bin = np.arange(mag_min, mag_max+0.2, 0.1)
num_mag = np.histogram(mag, mag_bin)[0]
cnum_mag = np.cumsum(num_mag[::-1])[::-1]

# 1. plot FMD 
plt.figure()
plt.semilogy(mag_bin[1:], num_mag, '^', markersize=mark_size)
plt.semilogy(mag_bin[1:], cnum_mag, '.', markersize=mark_size)
plt.xlabel('Magnitude', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
ax = plt.gca()
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title_fmd, fontsize=fsize_title)

# 2. plot M-t
plt.figure()
ax=plt.gca()
plt.scatter(ot, mag, alpha=alpha)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=20)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.ylabel('Magnitude', fontsize=fsize_label)
plt.title(fig_title_mt, fontsize=fsize_title)
plt.show()

