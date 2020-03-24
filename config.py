""" Configure file for seismicity visualization
"""
import os
import numpy as np

# 1. plot event location
class Config_Loc(object):
  def __init__(self):
    
    # catalog info
    self.ctlg_path = 'catalog/msms_reloc_fore.csv'
    self.fault_path = '/home/public/GMT_data/CN-faults.dat'
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
    self.line_wid = 1.

    
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

    
# 4. plot b-map
class Config_b_Map(object):
  def __init__(self):

    # catalog info
    self.ctlg_path = 'input/xls_pad_reloc.csv'
    self.fault_path = '/home/public/GMT_data/CN-faults.dat'
    self.lon_rng = [[102.5, 103.91], [102.3, 103.81]][1]
    self.lat_rng = [[24.3, 26.51], [26, 27.51]][1]
    # calc params
    self.xy_grid = 0.1
    self.slice_radius = [.25, 0.15][1]
    self.min_num = 200
    self.num_proc = 1
    self.max_b = 2.5
    self.min_mc = 0.3
    # plot params
    self.fig_fname = 'output/b_post-ld_pad.pdf'
    self.fig_title = 'Post-Ludian by PAD'
    self.fig_size = [(13, 16), (15,13)][1]
    self.fsize_label = 14
    self.fsize_title = 16
    self.mag_corr = .5
    self.mark_size = 4.
    self.alpha = 0.4
    self.cmap = 'viridis'
    self.cbar_asp = 10
    self.cbar_frac = [0.05, 0.03][1]
    self.cbar_pad = 0.02
    self.line_wid = 1.
    self.b_rng = [0.7, 2.3]
    self.mc_rng = [0.3, 1.1]
