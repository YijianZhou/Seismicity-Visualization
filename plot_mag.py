""" Plot FMD & M-t
"""
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime
from reader import read_ctlg
from statis_lib import *
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
alpha_fmd = cfg.alpha_fmd
alpha_mt = cfg.alpha_mt
mark_num = cfg.mark_num
mark_cum = cfg.mark_cum
color_num = cfg.color_num
color_cum = cfg.color_cum

# read & filter catalog
events = read_ctlg(ctlg_path)
mag_cond = (events['mag']>mag_rng[0])*(events['mag']<mag_rng[1])
events = events[mag_cond]
mag = np.array(list(events['mag']))
ot = [oti.datetime for oti in events['ot']]
# calc fmd
mag_bin, num, cum_num = calc_fmd(mag)
mc, [b_val, b_dev] = calc_mc_b(mag)
a_val = np.log10(sum(mag>mc))
gr_fit = 10**(a_val - b_val * (mag_bin - mc))
mag_bin_comp = mag_bin[mag_bin>=mc]
num_comp = num[mag_bin>=mc]
cum_num_comp = cum_num[mag_bin>=mc]
text_xy = (np.median(mag_bin), np.amax(cum_num_comp))

# 1. plot FMD 
plt.figure()
plt.semilogy(mag_bin, num, mark_num, markersize=mark_size, color=color_num, alpha=alpha_fmd)
plt.semilogy(mag_bin, cum_num, mark_cum, markersize=mark_size, color=color_cum, alpha=alpha_fmd)
plt.semilogy(mag_bin_comp, num_comp, mark_num, markersize=mark_size, color=color_num)
plt.semilogy(mag_bin_comp, cum_num_comp, mark_cum, markersize=mark_size, color=color_cum)
plt.semilogy(mag_bin, gr_fit, 'k--')
plt.annotate('Mc = %s \nb = %s $\pm$ %s'%(mc, b_val, b_dev), text_xy, fontsize=fsize_label)
plt.xlabel('Magnitude', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
ax = plt.gca()
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title_fmd, fontsize=fsize_title)

# 2. plot M-t
plt.figure()
ax=plt.gca()
plt.scatter(ot, mag, alpha=alpha_mt)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=20)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.ylabel('Magnitude', fontsize=fsize_label)
plt.title(fig_title_mt, fontsize=fsize_title)
plt.show()

