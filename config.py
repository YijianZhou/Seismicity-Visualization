""" Configure file for seismicity visualization
"""
import os
import numpy as np

# 1. plot event location
class Config_Loc(object):
  def __init__(self):

    # catalog info
    self.ctlg_path = 'catalog/msms_reloc_fore.csv'
    self.lon_rng = [-117.9, -117.2] 
    self.lat_rng = [35.4, 36.1] 
    self.dep_rng = [0, 20.]
    self.plot_prof = False
    self.prof_pnt = np.array([[-117.65,35.55],[-117.45,35.75]])
    self.prof_wd = 6. # width of profile km
    # plot params
    self.fig_title = 'MSMS HypoDD: Foreshock'
    self.fig_fname = 'output/msms_reloc_fore.pdf'
    self.prof_name = 'output/prof_msms_fore.pdf'
    self.fsize_label = 13
    self.fsize_title = 16
    self.mark_size = 3.
    self.alpha = 0.6
    self.fig_xsize = 7
    self.cmap = 'hot'
    self.cbar_pos = [0.8,0.65,0.03,0.25]
    self.cbar_ticks = np.arange(0,1.1,0.25)


# 2. plot FMD & M-t
class Config_Mag(object):
  def __init__(self):

    # catalog info
    self.ctlg_path = 'catalog/shelly_main.csv'
    self.mag_rng = [-1, 8.]
    # plot params
    self.fig_title_fmd = 'Shelly FMD: Ridgecrest'
    self.fig_title_mt = 'Shelly M-t: Ridgecrest'
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
    self.ctlg_list = ['catalog/scsn.csv', 'catalog/shelly.csv', 'catalog/pad.csv']
    self.name_list = ['SCSN', 'Shelly', 'PAD']
    self.color_list = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    self.mag_rng = [-1, 8.]
    # plot params
    self.fig_title_fmd = 'Compare FMD'
    self.fig_title_mt = 'Compare M-t'
    self.fsize_label = 14
    self.fsize_title = 16
    self.mark_size = 10.
    self.alpha_fmd = 0.6
    self.alpha_mt = 0.4
    self.mark_num = '^'
    self.mark_cum = '.'

