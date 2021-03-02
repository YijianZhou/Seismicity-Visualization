""" Plot conparison of phase picks
"""
import numpy as np
import matplotlib.pyplot as plt

# i/o paths
fpick = 'input/example.picks'
fout = 'output/example_pick-dev.pdf'
dt_max = 2
bins = np.arange(-dt_max, dt_max+0.01, 0.2)
# fig params
fig_size = (14,8)
fsize_label = 12
alpha = 0.8
xlabels = ['tp_pred - tp_target (sec)', 'ts_pred - ts_target (sec)']

dt_p, dt_s = [], []
n_fp, n_fs = 0, 0
f=open(fpick); lines=f.readlines(); f.close()
for line in lines:
    codes = line.split(',')
    tp_pred, ts_pred = [float(code) for code in codes[2:4]]
    tp_target, ts_target = [float(code) for code in codes[4:6]]
    if tp_pred==-1 or abs(tp_pred-tp_target)>dt_max: n_fp+=1
    else: dt_p.append(tp_pred-tp_target)
    if ts_pred==-1 or abs(ts_pred-ts_target)>dt_max: n_fs+=1
    else: dt_s.append(ts_pred-ts_target)
num_pha = len(lines)
std_p = np.std(dt_p)
mean_p = np.mean(dt_p)
std_s = np.std(dt_s)
mean_s = np.mean(dt_s)

# plot dt hist
plt.figure(figsize=fig_size)
ax = plt.subplot(121)
np,_,_ = plt.hist(dt_p, bins, edgecolor='tab:gray', alpha=alpha)
plt.xlabel(xlabels[0], fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.annotate('Detection Accuracy {:.2f}%\nPicking Precision {:.2f} $\pm$ {:.2f}s'.format(100-100*n_fp/num_pha, mean_p, std_p), (-dt_max, max(np)), fontsize=fsize_label, ha='left', va='top')
ax = plt.subplot(122, sharey=ax)
ns,_,_ = plt.hist(dt_s, bins, edgecolor='tab:gray', alpha=alpha)
plt.xlabel(xlabels[1], fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
plt.annotate('Detection Accuracy {:.2f}%\nPicking Precision {:.2f} $\pm$ {:.2f}s'.format(100-100*n_fs/num_pha, mean_s, std_s), (-dt_max, max(np)), fontsize=fsize_label, ha='left', va='top')
plt.tight_layout()
plt.savefig(fout)
