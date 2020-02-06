""" Configure file for seismicity visualization
"""
import os
import numpy as np

class Config(object):
  def __init__(self):

    # 1. plot event location
    # catalog info
    self.ctlg_path = '/home/zhouyj/Xiaojiang/run_pad/hypoinverse/output/zsy.csv'
    self.lon_rng = [102.5, 103.9] #[102.25, 103.8]
    self.lat_rng = [24.3, 26.5] #[25.9, 27.5]
    self.dep_rng = [0, 30.]
    # plot params
    self.fig_title = 'PAD HypoInverse: ZSY Network'
    self.fig_fname = 'zsy_pad_hyp.pdf'
    self.fsize_label = 14
    self.fsize_title = 16
    self.point_size = 3.
    self.alpha = 0.6
    self.fig_xsize = 5
    self.cmap = 'hot'
    self.cbar_pos = [0.76,0.6,0.03,0.25]
    self.cbar_ticks = np.arange(0,1.1,0.25)

