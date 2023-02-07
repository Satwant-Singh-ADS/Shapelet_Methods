# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 20:38:16 2022

@author: Batman
"""

from random import sample
import math

plt.rcParams.update({'font.size': 20})
#ShapeLet_Dictionary_State_level = {}
#Shapelet_dict_actual_state_week_vector_label = {}

#for keys in running_average.keys():
for keys in {'California', 'Florida', 'United States'}:
    
    State_name = keys
    if keys in Ignore_State_list:
        continue
    print(keys)
    running_avg = running_average[State_name]



    running_avg_vectors = []
    for i in range(len(running_avg)):
        if i<len(running_avg)-4:
            if i<=history_weeks:
                vec = running_avg[i:i+future_weeks+history_weeks]
            else:
                vec = running_avg[i-history_weeks:i+future_weeks]
#             vec = running_avg[i-history_weeks:i+future_weeks]
            vec1 = [w[1] for w in vec]

            week_nbr = vec[0][0]
            running_avg_vectors.append((week_nbr,vec1[0],vec1))

    dicy_state = Shapelet_dict_actual_state_week_vector_label.get(State_name,{})
#     print(dicy_state)
    
#    scenarios_list_pearson_perason = [(vector[0],vector[1],return_best_shapelet_pearson(vector[2], slope_thres[State_name]),return_all_shapelet_pearson(vector[2], slope_thres[State_name])) for vector in running_avg_vectors]
    scenarios_list_pearson_perason = ShapeLet_Dictionary_State_level[keys] 
    scenes_dict= {}
    for index,val in enumerate(list(set([w[2] for w in scenarios_list_pearson_perason]))):
        scenes_dict[val] = val[0]
    
    for vector in scenarios_list_pearson_perason:
        dicy_state[vector[0]] = [(vector[3],vector[2])]
 #   Shapelet_dict_actual_state_week_vector_label[State_name] = dicy_state
        

 #   ShapeLet_Dictionary_State_level[keys] = scenarios_list_pearson_perason

    ## Actual Covid tally plot validation 

    week_nbr_plt = [w[0] for w in scenarios_list_pearson_perason]
    actual_count_plt = [w[1] for w in scenarios_list_pearson_perason]
    labels_plt = [w[2] for w in scenarios_list_pearson_perason]


#     fig, ax = plt.subplots()
    fig, axs = plt.subplots(1,figsize=(24,8 ), dpi=200)
#     figure(figsize=(24,8 ), dpi=80)
    Week_nbr2 = week_nbr_plt
    str_week_int = []
    str_week = []
    reps = [[0.0]*len(Week_nbr2)]*len(shapelet_standard_names)
    reps = np.array(reps)
    for i in range(0,len(Week_nbr2)):
        reps[:, i] = dicy_state[Week_nbr2[i]][0][0]
    
    for i in range(0,len(Week_nbr2),5):
        str_week_int.append(Week_nbr2[i])
        str_week.append(date_formatting(Week_nbr2[i], t))
        

    axs.plot(week_nbr_plt,actual_count_plt)
    axs.set_xticks(str_week_int)
    axs.set_xticklabels(str_week,rotation=40,fontsize=20)
    axs.yaxis.set_tick_params(labelsize=20)
#     plt.se
    axs.set_xlabel('Forecasting Date', fontsize = 20)
    axs.set_ylabel('Smoothed Weekly '+Runtype, fontsize = 20)

#     axs.setxlabel("Week Number")
#     axs[0].ylabel("Covid-19 Case Volume")
    axs.set_title("Covid-19 "+Runtype+" Incidence plot with annotated shapelet Labels  -> {}".format(State_name),fontsize=25)
    
#     scenarios_list_pearson_perason_1 = sample(scenarios_list_pearson_perason,math.ceil(len(scenarios_list_pearson_perason)*0.95))
    for index,val in enumerate(scenarios_list_pearson_perason):
#         if index%2==0:
#             continue
        axs.text(val[0],val[1],scenes_dict[val[2]],fontsize=20,rotation=30)
    axs.text(0.2, 0.9,'Abbriviation Details',\
    horizontalalignment='center',\
    verticalalignment='center', transform = axs.transAxes,fontsize=20) 
    step=-0.1
    cnt=0
    for k11,v11 in scenes_dict.items():
        axs.text(0.2, 0.85+cnt*step,v11+ "-> "+k11,\
        horizontalalignment='center',\
        verticalalignment='center',transform = axs.transAxes,fontsize=20)  
        cnt+=0.4
        
        
    ax2 = axs.twinx()
    xx = (pd.DataFrame(Shapelet_shift[keys].items()))
    ax2.plot(week_nbr_plt[1:], xx[1], linestyle = 'dashed', color = 'green')
    ax2.set_ylabel('Trend Continuity')
    
    #perm_shapes = [3, 1, 5, 0, 4, 2]
    perm_shapes = [0, 1, 3, 2]
    rep_perm = reps[perm_shapes, :]
    fig, ax3 = plt.subplots(1,figsize=(24,8 ), dpi=200)
    ax3 = sns.heatmap(rep_perm)
    
    fig, ax4 = plt.subplots(1,figsize=(24,8 ), dpi=200)
    ax4.plot(week_nbr_plt,actual_count_plt)
    
    if export_visualizations:
        plt.savefig(Visualization_path+'Type : '+Runtype+'Shapelets_actual_cases_'+State_name+'.png')
    else:
        plt.show()