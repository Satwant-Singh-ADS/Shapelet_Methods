# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 22:47:13 2022

@author: Batman
"""

#state_lst = State_list_plotting[:]
state_lst = {'California', 'Florida'}

for state in state_lst:
    model = "Shapelet-ensemble"
#     if state not in ['California','United States']:
#         continue
    subset = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    fig, axs = plt.subplots(1,figsize=(25, 8 ), dpi=200)

    #fig.tight_layout(pad=13.0)

    subset_data = plot_results_softmax[plot_results_softmax['State_x']==state].drop_duplicates(['Week Number','Label_Actual_x'])
    Actual_Case_cnt = (subset_data['Covid_case_count']/subset_data['Count_overall']).to_list()

    Predicted_label = subset_data['Predicted'].to_list()

    Actual_Label = subset_data['Label_Actual_x'].to_list()

    Week_nbr = subset_data['Week Number'].to_list()
    str_week_int = []
    str_week = []
    for i in range(0,len(Week_nbr),5):
        str_week_int.append(Week_nbr[i])
        str_week.append(date_formatting(Week_nbr[i], t))

#         print(len(Week_nbr))
    a2 = axs.twinx()
    q = a2.plot(Week_nbr,Actual_Case_cnt[0:len(Week_nbr)],label="Weekly "+ Runtype,color="red")
#     a2.set_xlabel('Week', fontsize = 20)
    a2.set_ylabel('Smoothed Weekly '+Runtype, fontsize = 20)
    
#     axs[0].set(xlabel="Week", ylabel="Covid Case Count")

#     axs[0].set_title(Runtype+" Incidence over time for --> "+state,fontsize=23)
    a2.set_xticks(str_week_int)
    a2.set_xticklabels(str_week,rotation=40,fontsize=20)
    a2.yaxis.set_tick_params(labelsize=20)
#     axs[0].set_yticklabels(fontsize=13)
#     axs[0].set_yticks(Actual_Case_cnt)
#     axs[0].set_yticklabels(Actual_Case_cnt,fontsize=13)
    
    subset = MeanSimilarityModels[MeanSimilarityModels['State']==state]

    week_nbrs = list(subset['Week Number'].values)

    meanS_miliary = subset['Mean_Similarity'].values
    
    b = axs.plot(week_nbrs,meanS_miliary,label="IMA")
    axs.set_xlabel('Forecasting Date', fontsize = 20)
    axs.set_ylabel('Inter-model Agreement', fontsize = 20)
    axs.yaxis.set_tick_params(labelsize='large')
    axs.xaxis.set_tick_params(labelsize='large')
#     axs.xtick.labelsize(20)
#     axs.xaxis.set_size(20)
#     axs.set_yticklabels(fontsize=13)

#     axs[1].set(xlabel="Week Number", ylabel="Agreement score between Models")

    axs.set_title("Agreement between Models over time --> "+state,fontsize=23)
    
    leg1 = axs.legend(loc='upper left',prop={'size': 20})
    leg2 = a2.legend(loc='upper right',prop={'size': 20})
    
    plt.setp(axs.get_xticklabels(), rotation=30, horizontalalignment='right')
    if export_visualizations:
    
        plt.savefig(Visualization_path+"Agrrement_score_Paper_"+state+".png")
    else:
        plt.show()