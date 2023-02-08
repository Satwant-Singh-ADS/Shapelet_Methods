# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 16:46:31 2022

@author: Batman
"""
ensemble_model_name = "US-Flu\Flusight-ensemble"
 #%%  Prepare data for scatter plot 
state_lst = State_list_plotting[:] 
shape_change = []
perf_score_usc = []
perf_score_ensemble = []
for state in state_lst:    
    
    # Extract our ensemble and align with agreement score for this state
    xx = pd.DataFrame(Shapelet_shift[state].items(), columns = ['Week Number', 'Shape Cont'])
    xx1 = pd.DataFrame(State_week_avg_ensemble[state].items(),  columns = ['Week Number', 'Shape Ensemble'])
    xx2 = pd.merge(xx, xx1, how='inner', on='Week Number')
    # Extract COVIDhub ensemble and align with previous table
    xx1 = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    xx1 = xx1[xx1['Model Name']==ensemble_model_name]
    xx3 = pd.merge(xx2, xx1, how='inner', on='Week Number')
    
    shape_change = shape_change + (xx3['Shape Cont'].to_list())
    perf_score_ensemble = perf_score_ensemble + (xx3['Cosine Similarty'].to_list())
    perf_score_usc = perf_score_usc + (xx3['Shape Ensemble'].to_list())
    
    

    
#%% Show results
tc_cut_off = 0;
print('Performance at Total, Change vs Continued Trend')
print('Fraction when change is seen: ' )
print(len([i for i in range(len(shape_change)) if shape_change[i] <= tc_cut_off])/len(shape_change))
print('Shape Ensemble: ')
print(np.mean(perf_score_usc))
print(np.mean([perf_score_usc[i] for i in range(len(shape_change)) if shape_change[i] <= tc_cut_off]))
print(np.mean([perf_score_usc[i] for i in range(len(shape_change)) if shape_change[i] > tc_cut_off]))

print('Hub Ensemble: ')
print(np.mean(perf_score_ensemble))
print(np.mean([perf_score_ensemble[i] for i in range(len(shape_change)) if shape_change[i] <= 0.75]))
print(np.mean([perf_score_ensemble[i] for i in range(len(shape_change)) if shape_change[i] > 0.75]))
#%%
plt.rcParams.update({'font.size': 20})
fig, axs = plt.subplots(1,figsize=(12, 10), dpi=300)

usc = axs.scatter(shape_change, perf_score_usc, label="Shapelet Ensemble")
covid_ensemble = axs.scatter(shape_change, perf_score_ensemble,label="Hub Ensemble")

leg1 = axs.legend(loc='upper left')

axs.set_xlabel('Trend Contiuity', fontsize = 20)
axs.set_ylabel('Shapelet-space Score', fontsize = 20)


#     usc = axs[2].set(xlabel="Week", ylabel="Cosine Similarity",label = "USC Shapelet Ensemble")

#axs.set_title("Evaluation of Shapelet Ensemble & Hub-Ensemble using Agreement Score for State {}".format(state),fontsize=20)
if export_visualizations:
    plt.savefig(Visualization_path+"PlotType : "+Runtype+" "+'Evaluation of Shapelet Ensemble & Hub-Ensemble using Agreement Score for State '+state+'.png')
else:
    plt.show()



