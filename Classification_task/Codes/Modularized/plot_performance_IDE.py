# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 23:00:42 2022

@author: Batman
"""

#state_lst = State_list_plotting[:]
state_lst = {'California', 'Florida', 'United States'}

for state in state_lst:
    
    scatter_plot_x = None
    
    Scatter_plot_y1 = None
    
    Scatter_plot_y2 = None
    
    model = "USC shapelet-ensemble"
#     if state not in ['California','United States']:
#         continue
    subset = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    fig, axs = plt.subplots(1,figsize=(25, 8), dpi=200)

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
        str_week.append(date_formatting(Week_nbr[i]))

    data = State_week_avg_ensemble.get(state)
    
    x1 = []
    y1 = []
    for k,v in data.items():
        x1.append(k)
        y1.append(v)

    vectors = list(zip(x1,y1))

    vector_sorted = sorted(vectors,key = lambda x : x[0]) 

    x1 = [w[0] for w in vector_sorted ]
    y = [w[1] for w in vector_sorted ]
    Week_nbr = x1

    usc = axs.plot(x1,y,label='Shapelet Ensemble')
    scatter_plot_y1 = [x1,y]

    str_week_int = []
    str_week = []
    for i in range(0,len(Week_nbr),5):
        str_week_int.append(Week_nbr[i])
        str_week.append(date_formatting(Week_nbr[i]))
        
    axs.set_xticks(str_week_int)
    axs.set_xticklabels(str_week,rotation=40,fontsize=20)
    axs.yaxis.set_tick_params(labelsize=20)

    axs.set_xlabel('Forecasting Week', fontsize = 20)
    axs.set_ylabel('Shapelet-space Score', fontsize = 20)
    
    
#     usc = axs[2].set(xlabel="Week", ylabel="Cosine Similarity",label = "USC Shapelet Ensemble")

    axs.set_title("Model Evaluation for Shapelet Ensemble and COVID-hub Ensemble over time for State {}".format(state),fontsize=23)
#         plt.show()

    subset = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    subset_1 = subset[subset['Model Name']=='FH_COVIDhub_ensemble']
    
    x1 = subset_1['Week Number'].values
    
    y1 = subset_1['Cosine Similarty'].values
    
    
    vectors = list(zip(x1,y1))

    vector_sorted = sorted(vectors,key = lambda x : x[0]) 

    x = [w[0] for w in vector_sorted ]
    y = [w[1] for w in vector_sorted ]
    Week_nbr = x

    ensemble  = axs.plot(x,y,label="COVID-hub Ensemble")
    

#     axs[2].legend((usc,ensemble),('Perfis COPEX','Media'), loc = 'best')
    leg1 = axs.legend(loc='upper right',prop={'size': 20})
    a2 = axs.twinx()
    q = a2.plot(Week_nbr,Actual_Case_cnt[0:len(Week_nbr)],label="Case Incidence",color="red")
#     a2.set_xlabel('Week', fontsize = 20)
    a2.set_ylabel('Case Incidence per week', fontsize = 20)
    
#     axs[0].set(xlabel="Week", ylabel="Covid Case Count")

#     axs[0].set_title(Runtype+" Incidence over time for --> "+state,fontsize=23)
    a2.set_xticks(str_week_int)
    a2.set_xticklabels(str_week,rotation=40,fontsize=20)
    a2.yaxis.set_tick_params(labelsize=20)
    
    if export_visualizations:
        plt.savefig(Visualization_path+"PlotType : "+Runtype+" "+'Model_Evaluation Plot for Limited Models '+state+'.png')
    else:
        plt.show()
    
 #%%  Prepare data for scatter plot 
state_lst = State_list_plotting[:] 
ag_score = []
perf_score_usc = []
perf_score_ensemble = []
for state in state_lst:    
    
    # Extract our ensemble and align with agreement score for this state
    xx = MeanSimilarityModels[MeanSimilarityModels['State']==state]
    xx1 = pd.DataFrame(State_week_avg_ensemble[state].items())
    xx2 = pd.merge(xx, xx1, how='inner', left_on='Week Number', right_on=0)
    # Extract COVIDhub ensemble and align with previous table
    xx1 = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    xx1 = xx1[xx1['Model Name']=='FH_COVIDhub_ensemble']
    xx3 = pd.merge(xx2, xx1, how='inner', on='Week Number')
    
    ag_score = ag_score + (xx3['Mean_Similarity'].to_list())
    perf_score_ensemble = perf_score_ensemble + (xx3['Cosine Similarty'].to_list())
    perf_score_usc = perf_score_usc + (xx3[1].to_list())
    
    

    
#%% Plot performance vs 

plt.rcParams.update({'font.size': 20})
fig, axs = plt.subplots(1,figsize=(12, 10), dpi=300)

usc = axs.scatter(ag_score, perf_score_usc, label="Shapelet Ensemble")
covid_ensemble = axs.scatter(ag_score, perf_score_ensemble,label="COVID-hub Ensemble")

leg1 = axs.legend(loc='upper left')

axs.set_xlabel('Inter-model Agreement', fontsize = 20)
axs.set_ylabel('Shapelet-space Score', fontsize = 20)


#     usc = axs[2].set(xlabel="Week", ylabel="Cosine Similarity",label = "USC Shapelet Ensemble")

#axs.set_title("Evaluation of Shapelet Ensemble & COVID-hub-Ensemble using Agreement Score for State {}".format(state),fontsize=20)
if export_visualizations:
    plt.savefig(Visualization_path+"PlotType : "+Runtype+" "+'Evaluation of Shapelet Ensemble & COVID-hub-Ensemble using Agreement Score for State '+state+'.png')
else:
    plt.show()