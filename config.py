""" Configure file for seismicity visualization
"""
import os
import numpy as np

# 1. plot loc: loc map, profile & hist
class Config_Loc(object):
  def __init__(self):

    # catalog info
#    self.ctlg_path = '../hypoinverse/output/zsy.csv'
    self.ctlg_path = 'test/zsy.csv'
    self.lon_rng = [102.5, 103.9] #[102.25, 103.8]
    self.lat_rng = [24.3, 26.5] #[25.9, 27.5]
    self.dep_rng = [0, 30.]
    self.plot_prof = False
    self.prof_pnt = np.array([[103,25],[103.5,26]]) # ref points for profile
    self.prof_wd = 10. # width of profile km
    # plot params
#    self.fig_title = 'PAD HypoInverse: ZSY Network'
    self.fig_title = 'PAD Reloc: ZSY Network'
#    self.fig_fname = 'zsy_pad_hyp.pdf'
    self.fig_fname = 'zsy_pad_reloc.pdf'
    self.fsize_label = 13
    self.fsize_title = 16
    self.mark_size = 3.
    self.alpha = 0.6
    self.fig_xsize = 6
    self.cmap = 'hot'
    self.cbar_pos = [0.76,0.6,0.03,0.25]
    self.cbar_ticks = np.arange(0,1.1,0.25)


# 2. plot mag: FMD & M-t
class Config_Mag(object):
  def __init__(self):

    # catalog info
    self.ctlg_path = 'test/zsy.csv'
    self.mag_rng = [-1, 8.]
    # plot params
    self.fig_title_fmd = 'FMD: ZSY Network'
    self.fig_title_mt = 'M-t: ZSY Network'
    self.fsize_label = 14
    self.fsize_title = 16
    self.mark_size = 10.
    self.alpha_mt = 0.6
    self.alpha_fmd = 0.4
    self.mark_num = '^'
    self.mark_cum = '.'
    self.color_num = 'tab:blue'
    self.color_cum = 'tab:orange'


# 3. plot cmp: FMD
class Config_Cmp(object):
  def __init__(self):

    # catalog info
    self.ctlg_list = ['test/scsn.csv', 'test/shelly.csv']
    self.name_list = ['SCSN', 'Shelly']
    self.color_list = ['tab:blue', 'tab:orange']
    self.mag_rng = [-1, 8.]
    # plot params
    self.fig_title_fmd = 'Compare FMD: SCSN & Shelly'
    self.fig_title_mt = 'Compare M-t: SCSN & Shelly'
    self.fsize_label = 14
    self.fsize_title = 16
    self.mark_size = 10.
    self.alpha_fmd = 0.6
    self.alpha_mt = 0.4
    self.mark_num = '^'
    self.mark_cum = '.'


