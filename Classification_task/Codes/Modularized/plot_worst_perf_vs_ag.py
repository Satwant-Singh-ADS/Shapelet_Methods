# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 16:04:43 2022

@author: Batman
"""
# Must run plot_performance_IDE first
ag_thres = []
worst_ensemble = []
worst_usc = []
num_ags = []
for j in range (-10, 11):
    this_ag_thres = j*0.1
    try:
        this_worst_ensemble = np.min([perf_score_ensemble[i] for i in range(len(ag_score)) if ag_score[i]>=this_ag_thres])
    except:
        this_worst_ensemble = float("nan")
        
    try:    
        this_worst_usc = np.min([perf_score_usc[i] for i in range(len(ag_score)) if ag_score[i]>=this_ag_thres])
    except:
        this_worst_usc = float("nan")
        
    this_num_ags = len([i for i in range(len(ag_score)) if ag_score[i]>=this_ag_thres])
    ag_thres = ag_thres + [this_ag_thres]
    worst_ensemble = worst_ensemble + [this_worst_ensemble]
    worst_usc = worst_usc + [this_worst_usc]
    num_ags = num_ags + [this_num_ags]
        
num_ags = [num_ags[i]/num_ags[0] for i in range(len(num_ags))]    
#%% plot
plt.rcParams.update({'font.size': 22})
fig, axs = plt.subplots(1,figsize=(12, 10), dpi=300)
axs.plot(ag_thres, worst_usc, label="Shapelet Ensemble")
axs.plot(ag_thres, worst_ensemble, label="Hub Ensemble")
axs.set_xlabel('Agreement Threshold')
axs.set_ylabel('Worst-case Performance')
axs.legend(loc= 'center left')

axs2 = axs.twinx()
axs2.plot(ag_thres, num_ags, label="Coverage", color='black', linestyle='dashed')
axs2.set_ylabel('Threshold Coverage')
axs2.legend(loc='center right')