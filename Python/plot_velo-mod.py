import numpy as np
import matplotlib.pyplot as plt

# i/o paths
fout = 'output/eg_velo-mod.pdf'
dep_list = [[0,1,2,4,6,8,10,12,16,20,25,30,37,45],
    [0,2,8,12,16,20,24,28,32,34,38,42],
    [0,3,4,5,9,12,16,20,25,34,36]]
last_dep = 50
vp_list = [[3.88,4.52,5.62,5.75,5.85,5.96,6.00,6.05,6.32,6.40,6.83,6.89,7.80,8.22],
    [4.85,5.72,5.77,5.84,6.08,6.19,6.28,6.40,7.40,7.55,7.84,7.95],
    [5.0,5.3,5.6,5.75,5.85,5.95,6.25,6.35,6.55,7.2,7.8]]
vs_list = [1.73,[2.78,3.28,3.31,3.36,3.52,3.57,3.61,3.68,4.18,4.34,4.38,4.52],1.73]
num_mod = len(dep_list)
names = ['Guvercin et al. (2022)','Acarel et al. (2019)','This study']
colors = ['tab:blue','tab:green','tab:red']
# fig config
fig_size = (16*0.8, 10*0.8)
fsize_label = 14
fsize_title = 18
alpha = 0.8
line_wid = 2.

def plot_label(xlabel=None, ylabel=None, title=None, xvis=True, yvis=True):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(ax.xaxis.get_majorticklabels(), fontsize=fsize_label, visible=xvis)
    plt.setp(ax.yaxis.get_majorticklabels(), fontsize=fsize_label, visible=yvis)

plt.figure(figsize=fig_size)
ax = plt.subplot(121)
ax.invert_yaxis()
for ii in range(num_mod):
  dep = [dep for dep in dep_list[ii] for _ in range(2)]; dep += [last_dep]; del dep[0]
  vp = [vp for vp in vp_list[ii] for _ in range(2)]
  plt.plot(vp, dep, color=colors[ii], lw=line_wid, alpha=alpha, label=names[ii])
plt.legend(fontsize=fsize_label, loc='lower left')
plot_label('Vp (km/s)', 'Depth (km)')
ax = plt.subplot(122)
ax.invert_yaxis()
for ii in range(num_mod):
  dep = [dep for dep in dep_list[ii] for _ in range(2)]; dep += [last_dep]; del dep[0]
  if not type(vs_list[ii])==list: vs = [vp/vs_list[ii] for vp in vp_list[ii] for _ in range(2)]
  else: vs = [vs for vs in vs_list[ii] for _ in range(2)]
  plt.plot(vs, dep, color=colors[ii], lw=line_wid, alpha=alpha)
plot_label('Vs (km/s)', yvis=False)
# save fig
plt.tight_layout()
plt.savefig(fout)
