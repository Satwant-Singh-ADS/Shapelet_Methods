# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 16:46:31 2022

@author: Batman
"""
 #%%  Prepare data for scatter plot 
state_lst = State_list_plotting[:] 
shape_change = []
perf_score_usc = []
perf_score_ensemble = []
for state in state_lst:    
    
    # Extract our ensemble and align with agreement score for this state
    xx = pd.DataFrame(Shapelet_shift['Texas'].items(), columns = ['Week Number', 'Shape Cont'])
    xx1 = pd.DataFrame(State_week_avg_ensemble[state].items(),  columns = ['Week Number', 'Shape Ensemble'])
    xx2 = pd.merge(xx, xx1, how='inner', on='Week Number')
    # Extract COVIDhub ensemble and align with previous table
    xx1 = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
    xx1 = xx1[xx1['Model Name']=='FH_COVIDhub_ensemble']
    xx3 = pd.merge(xx2, xx1, how='inner', on='Week Number')
    
    shape_change = shape_change + (xx3['Shape Cont'].to_list())
    perf_score_ensemble = perf_score_ensemble + (xx3['Cosine Similarty'].to_list())
    perf_score_usc = perf_score_usc + (xx3['Shape Ensemble'].to_list())
    
    

    
#%% Show results

print('Performance at Total, Change vs Continued Trend')
print('Fraction when change is seen: ' )
print(len([i for i in range(len(shape_change)) if shape_change[i] <= 0])/len(shape_change))
print('Shape Ensemble: ')
print(np.mean(perf_score_usc))
print(np.mean([perf_score_usc[i] for i in range(len(shape_change)) if shape_change[i] <= 0]))
print(np.mean([perf_score_usc[i] for i in range(len(shape_change)) if shape_change[i] > 0]))

print('COVIDhub Ensemble: ')
print(np.mean(perf_score_ensemble))
print(np.mean([perf_score_ensemble[i] for i in range(len(shape_change)) if shape_change[i] <= 0]))
print(np.mean([perf_score_ensemble[i] for i in range(len(shape_change)) if shape_change[i] > 0]))
