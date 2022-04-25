import os, glob, sys
sys.path.append('/home/zhouyj/software/data_prep')
from obspy import read, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
from signal_lib import preprocess 
from reader import read_fpha, dtime2str, get_data_dict
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fpha = 'input/fpha_eg.csv'
evid = 1 # use event index to select which event to plot
chn_idx = 2
data_dir = 'input/Example_data'
get_data_dict = get_data_dict
# get event info
event_loc, pick_dict = read_fpha(fpha)[evid]
ot = event_loc[0]
event_name = dtime2str(ot)
data_dict = get_data_dict(ot, data_dir)
fout = 'output/eg_wave-tp_%s.pdf'%event_name
title = 'Waveform Alignment with P Arrival: %s'%event_name
# data preprocess
samp_rate = 100
win_len = [10,30]
npts = int(samp_rate * sum(win_len))
time = -win_len[0] + np.arange(npts) / samp_rate
freq_band = [1,20]
num_sta = 20
# fig config
fig_size = (12,9)
fsize_label = 14
fsize_title = 18
line_wid = 1.
alpha = 0.8

# sort pick by epicentral distance
dtype = [('sta','O'),('tp','O')]
picks = [(sta,tp) for sta, [tp,ts] in pick_dict.items()]
picks = np.array(picks, dtype=dtype)
picks = [pick for pick in picks if pick['sta'] in data_dict]
picks = np.sort(picks, order='tp')[0:num_sta]

def plot_label(xlabel=None, ylabel=None, title=None):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(plt.gca().xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(plt.gca().yaxis.get_majorticklabels(), fontsize=fsize_label)

plt.figure(figsize=fig_size)
for ii,[sta,tp] in enumerate(picks):
    data_path = data_dict[sta][chn_idx]
    st = read(data_path)
    st = preprocess(st.slice(tp-win_len[0], tp+win_len[1]), samp_rate, freq_band)
    st_data = st.normalize()[0].data[0:npts] + ii*2
    plt.plot(time, st_data, lw=line_wid)
plt.vlines(0, -1, 2*ii+1, 'r', zorder=0)
plt.yticks(np.arange(len(picks))*2, picks['sta'], fontsize=fsize_label)
plot_label('Time (s)', None, title)
plt.tight_layout()
plt.savefig(fout)
