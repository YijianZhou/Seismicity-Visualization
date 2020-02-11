""" Plot catalog comparison
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import config
from reader import read_ctlg, slice_ctlg
from statis_lib import calc_fmd

# read & filter catalog
def get_mag_ot(ctlg_path):
    events = read_ctlg(ctlg_path)
    events = slice_ctlg(events, mag_rng=mag_rng)
    mag = np.array(list(events['mag']))
    ot = [oti.datetime for oti in events['ot']]
    return mag, ot


# catalog info
cfg = config.Config_Cmp()
mag_rng = cfg.mag_rng
ctlg_list = cfg.ctlg_list
mags, ots = [], []
for ctlg in ctlg_list:
    magi, oti = get_mag_ot(ctlg)
    mags.append(magi)
    ots.append(oti)

# plot config
name_list = cfg.name_list
color_list = cfg.color_list
fig_title_fmd = cfg.fig_title_fmd
fig_title_mt = cfg.fig_title_mt
fsize_label = cfg.fsize_label
fsize_title = cfg.fsize_title
mark_size = cfg.mark_size
alpha_fmd = cfg.alpha_fmd
alpha_mt = cfg.alpha_mt
mark_num = cfg.mark_num
mark_cum = cfg.mark_cum


# 1. plot FMD 
plt.figure()
p_list = []
for i in range(len(mags)):
    mag_bin, num, cum_num = calc_fmd(mags[i])
    pi = plt.semilogy(mag_bin, num, mark_num, markersize=mark_size, color=color_list[i], alpha=alpha_fmd)
    pi+= plt.semilogy(mag_bin, cum_num, mark_cum, markersize=mark_size, color=color_list[i], alpha=alpha_fmd)
    p_list.append(pi[0])
plt.legend(p_list, name_list, fontsize=fsize_label)
plt.xlabel('Magnitude', fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
ax = plt.gca()
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.title(fig_title_fmd, fontsize=fsize_title)

# 2. plot M-t
plt.figure()
ax = plt.gca()
p_list = []
for i in range(len(mags)):
    pi = plt.scatter(ots[i], mags[i], color=color_list[i], alpha=alpha_mt)
    p_list.append(pi)
plt.legend(p_list, name_list, fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, rotation=20)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.ylabel('Magnitude', fontsize=fsize_label)
plt.title(fig_title_mt, fontsize=fsize_title)
plt.show()

