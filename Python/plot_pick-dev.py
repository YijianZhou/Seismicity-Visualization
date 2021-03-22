""" Plot conparison of phase picks
"""
import numpy as np
import matplotlib.pyplot as plt

# i/o paths
fpicks = ['input/example1.picks', 'input/example2.picks']
fout = 'output/example_pick-dev.pdf'
dt_max = 1
bins = np.arange(-dt_max, dt_max+0.01, 0.1)
# fig params
fig_size = (16*0.8,9*0.8)
fsize_label = 12
fsize_title = 16
alpha = 0.6
names = ['Pick 1','Pick 2']
title = 'Phase Picking Comparison'
xlabels = ['tp_pred - tp_target (sec)', 'ts_pred - ts_target (sec)']
subplot_rect = {'left':0.08, 'right':0.98, 'bottom':0.08, 'top':0.94, 'wspace':0.05, 'hspace':0.}
colors = ['tab:blue','tab:orange']

def hist_pick(fpick):
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
    return dt_p, dt_s, 100*(1-n_fp/num_pha), 100*(1-n_fs/num_pha), [mean_p,std_p], [mean_s,std_s]

dt_p, dt_s, det_p, det_s, prec_p, prec_s = [],[],[],[],[],[]
for fpick in fpicks:
    dt_p_i, dt_s_i, det_p_i, det_s_i, prec_p_i, prec_s_i = hist_pick(fpick)
    dt_p.append(dt_p_i)
    dt_s.append(dt_s_i)
    det_p.append(det_p_i)
    det_s.append(det_s_i)
    prec_p.append(prec_p_i)
    prec_s.append(prec_s_i)
num_s, num_p = np.zeros([2,len(fpicks),len(bins)-1])

# plot dt hist
plt.figure(figsize=fig_size)
ax = plt.subplot(121)
for i in range(len(fpicks)):
    num_p[i],_,_ = plt.hist(dt_p[i], bins, color=colors[i], edgecolor='tab:gray', alpha=alpha, label=names[i])
plt.xlabel(xlabels[0], fontsize=fsize_label)
plt.ylabel('Number', fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label)
det_acc = '  '.join(['{:.2f}%\n'.format(acc) for acc in det_p])
pick_prec = '  '.join(['{0[0]:.2f} $\pm$ {0[1]:.2f}s\n'.format(prec) for prec in prec_p])
plt.annotate('Detection Accuracy:\n  {}\nPicking Precision:\n  {}'.format(det_acc, pick_prec),
    (-dt_max, np.amax(num_p)), fontsize=fsize_label, ha='left', va='top')
ax.legend(fontsize=fsize_label)
ax = plt.subplot(122, sharey=ax)
for i in range(len(fpicks)):
    num_s[i],_,_ = plt.hist(dt_s[i], bins, color=colors[i], edgecolor='tab:gray', alpha=alpha, label=names[i])
plt.xlabel(xlabels[1], fontsize=fsize_label)
plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label)
plt.setp(ax.yaxis.get_majorticklabels(), visible=False)
det_acc = '  '.join(['{:.2f}%\n'.format(acc) for acc in det_s])
pick_prec = '  '.join(['{0[0]:.2f} $\pm$ {0[1]:.2f}s\n'.format(prec) for prec in prec_s])
plt.annotate('Detection Accuracy:\n  {}\nPicking Precision:\n  {}'.format(det_acc, pick_prec),
     (-dt_max, np.amax(num_p)), fontsize=fsize_label, ha='left', va='top')
plt.suptitle(title, fontsize=fsize_title)
plt.subplots_adjust(**subplot_rect)
plt.savefig(fout)
