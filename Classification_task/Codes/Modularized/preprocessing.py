from Similarity_fxns import *

#%%
##################### Preprocessing Code ###########################################

state_population = pd.read_csv(Actual_incidence_path+"US State Population.csv")

state_population.dtypes

population_dictionary = state_population.set_index("State").to_dict()["Population"]

### This file contains incremental day on day cumulative cases across different states
cases_tmp = pd.read_csv(Actual_incidence_path+"US_actual_data.csv")

US_total = pd.DataFrame(cases_tmp.sum(axis=0))

cases = pd.concat([cases_tmp,US_total.T], ignore_index=True)

impute = {}

impute['Country'] = {'WashingtonIllinoisCaliforniaArizonaMassachusettsWisconsinTexasNebraskaUtahOregonFloridaNew YorkRhode IslandGeorgiaNew HampshireNorth CarolinaNew JerseyColoradoMarylandNevadaTennesseeHawaiiIndianaKentuckyMinnesotaOklahomaPennsylvaniaSouth CarolinaDistrict of ColumbiaKansasMissouriVermontVirginiaConnecticutIowaLouisianaOhioMichiganSouth DakotaArkansasDelawareMississippiNew MexicoNorth DakotaWyomingAlaskaMaineAlabamaIdahoMontanaPuerto RicoVirgin IslandsGuamWest VirginiaNorthern Mariana IslandsAmerican Samoa':"United States"}

cases = cases.replace(impute)


#%%
N = 397
t = 'Sep 1 2021'
format = '%b %d %Y'
now = datetime.strptime(t,format)
after = now + timedelta(days = N)
print(now)
print(after)

cases_for_use = cases.iloc[:,N:]
cases_for_slope_thres = cases.iloc[:,(N%7):N].T
start = N
days = [i for i in range(start,start+cases_for_use.shape[1])]
cases_for_use.columns = days
weekly_cases = pd.DataFrame()

for i in range(start, start+cases_for_use.shape[1],7):
    weekly_cases = pd.concat([weekly_cases,cases_for_use[i]],axis=1)
  
weekly_cases_2 = weekly_cases.copy()
weekly_cases_2 = weekly_cases.diff(axis=1)
weekly_cases_2[weekly_cases_2<0] = 0
weekly_cases1 = weekly_cases_2[list(weekly_cases_2.columns)[1:]]

weekly_cases1.index = list(cases['Country'].values)
states_list = list(cases['Country'].values)

days = [i for i in range(0,cases_for_slope_thres.shape[1])]
cases_for_slope_thres.columns = days

slope_thres = {}
for i in range(len(states_list)):
    slope_thres[states_list[i]] = np.max([1, np.max(cases_for_slope_thres[i].diff(periods=3)/3)])

Actual_covid_tally = weekly_cases1.copy()
# 2020-6-28 is a Sunday

JHU_actual_pd = Actual_covid_tally.copy()

data_array = JHU_actual_pd.values

week_numbers = JHU_actual_pd.columns

pd.set_option('display.max_columns', None)
#JHU_actual_pd

Actual_covid_tally_dict = Actual_covid_tally.T.to_dict()

#%% Using a sliding window, compute the runnning averages of fixed window sizes


state_wise_running_averages = []

for state in range(len(states_list)):
    vector = data_array[state]
    running_average = [0]*len(vector)
    xx = pd.DataFrame(vector).rolling(window= 3, min_periods=1, center=True).mean()
    running_average = xx[0].tolist()
    
    state_wise_running_averages.append(running_average)
    
        
running_average={}
for state in range(len(states_list)):
    
    running_average[states_list[state]] = list(zip(week_numbers,state_wise_running_averages[state]))    
orignial_1 = data_array[0]

len(orignial_1)

len(state_wise_running_averages[0])

x = list(range(len(orignial_1)))

len(x)


fig, axs = plt.subplots(1,figsize=(15,8 ), dpi=80)
ensemble  = plt.plot(x,orignial_1,label="Actual Case Incidence Line")
#     axs[2].legend((usc,ensemble),('Perfis COPEX','Media'), loc = 'best')
ensemble  = plt.plot(x,state_wise_running_averages[0],label="3 Weeks Average smoothened Incidence Line")
#     axs[2].legend((usc,ensemble),('Perfis COPEX','Media'), loc = 'best')
leg1 = plt.legend(loc='upper right',prop={'size': 13})

plt.title("Average Smoothening of Ground Truth Data", fontsize = 20)

plt.ylabel("Case Incidence per Week",fontsize = 20)

plt.xlabel("Week Number",fontsize = 20)
leg1 = plt.legend(loc='upper right',prop={'size': 13})

if export_visualizations:
    plt.savefig(Visualization_path+"Average_smoothening_demo.png")
else:
    print("**")

#%%%%% Generating Shapelets for Actual Covid-19 Case/Death Incidence - Ground Truth


# shapelet_Combinatinos = list(combinations(shapelet_standard_array,2))

# shapelet_Combinatinos_names = list(combinations(shapelet_standard_names,2))



# pairwise_dissimilairty = {}
# for i in range(len(shapelet_Combinatinos_names)):
#     vector1 = shapelet_Combinatinos[i][0]
#     vector2 = shapelet_Combinatinos[i][1]
#     pairwise_dissimilairty[shapelet_Combinatinos_names[i]]  = spatial.distance.cosine(vector1,vector2)
    
    

# overall_sum = sum(pairwise_dissimilairty.values())
# for k,v in pairwise_dissimilairty.items():
#     pairwise_dissimilairty[k] = v/overall_sum
    
    

# with open(pickle_path+'ShapeLet_loss_weight.pickle', 'wb') as handle:
#     pickle.dump(pairwise_dissimilairty, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
### Lets Generate for each week/ state, running vectors of size 5

ShapeLet_Dictionary_State_level = {}
Shapelet_shift ={}

Shapelet_dict_actual_state_week_vector_label = {}

for keys in running_average.keys():
#     print(keys)
    State_name = keys
    running_avg = running_average[State_name]



    running_avg_vectors = []
    for i in range(len(running_avg)):
        if i<len(running_avg)-future_weeks:
            if i<=history_weeks:
                vec = running_avg[i-0:i+future_weeks+history_weeks]
            else:
                vec = running_avg[i-history_weeks:i+future_weeks]
            vec1 = [w[1] for w in vec]
            assert len(vec1)==Shapelet_length,"Size of vector not equal to standard shapelet size"


            week_nbr = vec[0][0]
            running_avg_vectors.append((week_nbr,vec1[0],vec1))

    dicy_state = Shapelet_dict_actual_state_week_vector_label.get(State_name,{})
#     print(dicy_state)
#     assert len(vector[2])==Shapelet_length,"Size of vector not equal to standard shapelet size"
    scenarios_list_pearson_perason = [(vector[0],vector[1],return_best_shapelet_pearson(vector[2], slope_thres[State_name]),return_all_shapelet_pearson(vector[2], slope_thres[State_name])) for vector in running_avg_vectors]
    
    for vector in scenarios_list_pearson_perason:
        dicy_state[vector[0]] = [(vector[3],vector[2])]
    Shapelet_dict_actual_state_week_vector_label[State_name] = dicy_state
        

    ShapeLet_Dictionary_State_level[keys] = scenarios_list_pearson_perason
    
    this_shift = {}
    for i in range(2,len(running_avg)-future_weeks+1):
        prev_shape = Shapelet_dict_actual_state_week_vector_label[keys][start+ 7*(i-1)][0][0]
        this_shape = Shapelet_dict_actual_state_week_vector_label[keys][start+ 7*i][0][0]
        this_shift[7*i+start] = cosine_sim(prev_shape, this_shape)
   

    Shapelet_shift[keys] = this_shift
    
    week_nbr_plt = [w[0] for w in scenarios_list_pearson_perason]
    actual_count_plt = [w[1] for w in scenarios_list_pearson_perason]
    labels_plt = [w[2] for w in scenarios_list_pearson_perason]




    
#import pickle

with open(pickle_path+'ShapeLet_Dictionary_State_level_actual.pickle', 'wb') as handle:
    pickle.dump(ShapeLet_Dictionary_State_level, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#import pickle

with open(pickle_path+'Shapelet_dict_actual_state_week_vector_label.pickle', 'wb') as handle:
    pickle.dump(Shapelet_dict_actual_state_week_vector_label, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#%% Load Models Data and apply Shapelets method on it

if Data_refresh==1:
    print("Data refresh process begins")
    
    root = [w for w in root_tmp if w.split("/")[-1] not in Ignore_model_list]

    len(root)

    model_lookup = {}


    for l in root[:]:
        model_lookup1 = {}
    #     try:
        df_master = pd.DataFrame()
    #     print(l)

        subroot = glob.glob(l+"/*.csv")
        for k in subroot:
    #         print(k)
    #         print(k)
            df = pd.read_csv(k).fillna(0)
            if len(df["State"])<2:
                continue
            
            US_total_1 = pd.DataFrame(df.sum(axis=0))

            df = pd.concat([df,US_total_1.T])
            df.loc[df["State"].str.len() > 100,"State"] = "United States"

            temp = re.findall(r'\d+', k.split("/")[-1])[-1]

            res = temp
            model_lookup1[res] = df
        model_lookup[l.split("/")[-1]] = model_lookup1

    print("Total Number of Models in Repository ---> {}".format(len(model_lookup.keys())))

    

    Eligible_Model_week_State_forecasts= {}

    for key, val in model_lookup.items():
        if len(val)>qualifying_threshold:
            Eligible_Model_week_State_forecasts[key] = val

    #import pickle

    with open(pickle_path+'Eligible_Model_week_State_forecasts.pickle', 'wb') as handle:
        pickle.dump(Eligible_Model_week_State_forecasts, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Data Refresh process for Model Forecasts completed")
else:
    print("Using Pickle file already gnerated in the past")
    file = open(pickle_path+'Eligible_Model_week_State_forecasts.pickle','rb')
    Eligible_Model_week_State_forecasts = pickle.load(file)

    print("Total Number of Eligible Models in Repository ---> {}".format(len(Eligible_Model_week_State_forecasts.keys())))



   #%% 
########### RUnning loop at State-Model_week level to generate correlation of model forecast with standard shapes


State_model_Week_vector_shapelet_Actual_dict = {}

model_wise_master_db =[]

ddd = 0

impu = 0 

model_cnt = 0


for key_outer,value_outer in Eligible_Model_week_State_forecasts.items():
#     if key_outer!='USC_SI_kJalpha':
#         continue
    model_lookup1 = value_outer
    iters = list(model_lookup1.keys())
    for key in iters:
#         if key!='327':
#             continue
        
        data = model_lookup1[key]
        cols = list(data.columns)
        
            
        start_index = cols.index("State")
        forecast_start = start_index+2
        forecast_end = forecast_start+4
        valid_columns = [cols[start_index]]+cols[forecast_start:forecast_end]
        if len(cols)<=6:
            valid_columns = [cols[start_index]]+cols[start_index+1:]
        forecast_input = data[valid_columns]
        state_iterations = list(forecast_input['State'].values)

        for state in state_iterations:
            if state in Ignore_State_list:
                continue
#             if state!='California':
#                 continue
            try:
                predictions_raw = forecast_input[forecast_input['State']==state][:].values[0][1:]
            except:
                print(key_outer,key,state)
                predictions_raw = forecast_input[forecast_input['State']=="Virgin Islands, U.S."][:].values[0][1:]
            week_num = int(key)
            mod = week_num%7
            target = N%7
            add = target-mod
            lookup_key = add+week_num
            try:
                actual_covid_tally_records = Actual_covid_tally_dict[state]
            except:
                actual_covid_tally_records = Actual_covid_tally_dict["Virgin Islands"]
            week_num = int(key)
            if history_weeks>0:
                ddd+=1
#                 print("History >0")
                mod = week_num%7
                target = N%7
                add = target-mod

                lookup_key = add+week_num
                history_vector = []
                for h1 in range(history_weeks):
                    history1 = actual_covid_tally_records.get(lookup_key-7*(h1+1),None)
                    if history1 is None:
                        history_vector.append(predictions_raw[0])
                        impu+=1
#                         print("imputation performed")
                    else:
                        history_vector.append(history1)
                history_vector.reverse()
                predictions_vector_tmp = history_vector+list(predictions_raw) 
                predictions_vector_tmp_1 = predictions_vector_tmp[:-1]+[predictions_vector_tmp[-1]+0.00001]

    #             try:
    #             print(state,lookup_key,key_outer)
                if predictions_vector_tmp[0] is None:
                    predictions_vector_tmp = [predictions_vector_tmp[1]]+predictions_vector_tmp[1:]

                if len(predictions_vector_tmp)!=Shapelet_length:
#                     print("Skipped Evaluation")
                    continue
                    
    #             print(lookup_key)
    #             print(key)
    #             print("Vector Used : ",predictions_vector_tmp)
            else:
                predictions_vector_tmp = list(predictions_raw[:])
                if len(predictions_vector_tmp)!=Shapelet_length:
                    print("Skipped Evaluation",week_num,state,key_outer)
                    
                    continue
            if key_outer=='FH_COVIDhub_baseline':
#                 print(key,state,predictions_vector_tmp)
                continue
            state_dict = State_model_Week_vector_shapelet_Actual_dict.get(state,{})
            
            state_dict_model_dict = state_dict.get(lookup_key,{})
            try:
                Actual_shapelte_5X1_vector = Shapelet_dict_actual_state_week_vector_label[state][lookup_key][0]
            except:
                Actual_shapelte_5X1_vector = [None]*Shapelet_length
#                 print("exception",key,state,predictions_vector_tmp)
                continue
            shape_1 = return_best_shapelet_pearson(predictions_vector_tmp, slope_thres[state])
#             try:
            state_dict_model_dict[key_outer] = [((return_all_shapelet_pearson(predictions_vector_tmp, slope_thres[state]),Actual_shapelte_5X1_vector,),shape_1)]
#             except:
                
            state_dict[lookup_key] = state_dict_model_dict
            
            State_model_Week_vector_shapelet_Actual_dict[state] = state_dict
#             print("Shape Predicted: ",shape)
            model_wise_master_db.append((state,lookup_key,key_outer,shape_1))
#             except:
#             print(state,lookup_key,key_outer,shape)


# 612 - USC - what


print("Total Number of Iterations {}".format(ddd))
print("Total number of impuations {}".format(impu))



with open(pickle_path+'State_model_Week_vector_shapelet_Actual_dict.pickle', 'wb') as handle:
    pickle.dump(State_model_Week_vector_shapelet_Actual_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    
#%%
Actual_covid_tuples = []

for key, val1 in ShapeLet_Dictionary_State_level.items():
    for val in val1:
        Actual_covid_tuples.append((key,val[0],val[1],val[2]))
        
Actual_covid_df = pd.DataFrame(Actual_covid_tuples)




Actual_covid_df.columns  = ['State','Week_number','Covid Count','Label_Actual']

Actual_covid_df['key'] = Actual_covid_df['State']+"_"+Actual_covid_df['Week_number'].astype("str")



model_wise_master_df = pd.DataFrame(model_wise_master_db)

model_wise_master_df.columns = ['State','Week Number','Model_Name','Predicted']

model_wise_master_df['key'] = model_wise_master_df['State']+"_"+model_wise_master_df['Week Number'].astype("str")



merged_df_models_actual = model_wise_master_df.merge(Actual_covid_df,how='inner',on='key')


print(Actual_covid_df['Label_Actual'].value_counts())

print(model_wise_master_df['Predicted'].value_counts()/model_wise_master_df['Model_Name'].nunique())

merged_df_models_actual.to_csv(Ouput_path+"Shapelet_model_evaluation_cases.csv")



State_weel_ScenarioWise = merged_df_models_actual.groupby(['State_x',"Week Number","Predicted","Label_Actual"]).agg(Count = ("Week_number","count")).reset_index()




State_week_rolllup = merged_df_models_actual.groupby(['State_x',"Week Number","Label_Actual"]).agg(Count_overall = ("Week_number","count"),Covid_case_count= ("Covid Count","sum")).reset_index()


Summarized_Results = State_weel_ScenarioWise.merge(State_week_rolllup,on=['State_x','Week Number'],how="inner").drop(["Label_Actual_y"],axis=1)


Summarized_Results['Probability of Class'] = Summarized_Results['Count']/Summarized_Results['Count_overall']



Summarized_Results["rank"] = Summarized_Results.groupby(["State_x","Week Number"])["Probability of Class"].rank("dense", ascending=False)


plot_results_softmax = Summarized_Results[Summarized_Results['rank']==1]

State_Iteration = list(plot_results_softmax.State_x.unique())

import pandas as pd

merged_df_models_actual = pd.read_csv(Ouput_path+"Shapelet_model_evaluation_cases.csv")

Master_df_actual_VS_Model_Agrrement = pd.DataFrame()

#%%
a = set()
for State_name in State_model_Week_vector_shapelet_Actual_dict.keys():
    if State_name in Ignore_State_list:
        continue



    State_Week_Model_name_Cosine_match_cases = {}
    # State_name = 'California'



    # California_debug_actual = Shapelet_dict_actual_state_week_vector_label[State_name]

    California_debug_model =  State_model_Week_vector_shapelet_Actual_dict[State_name]


    generate_tuple = []

    state_dict = State_Week_Model_name_Cosine_match_cases.get(State_name,{})


    for weeks, model_level in California_debug_model.items():
#         if weeks>585:
#             continue
        week_dict = state_dict.get(weeks,{})
        
        

        for model,data_vector in model_level.items():
#             if model!='FH_COVIDhub_ensemble':
#                 pass
    #         print(data_vector)
            datset1 = data_vector[0][0][0]
            dataset2 = data_vector[0][0][1][0]
    #         print(data_vector[0][0][1][1])
    #         print(data_vector[0][1])
            model_val = week_dict.get(model,None)
            if model_val is None:
                try:
                    week_dict[model] =(data_vector[0][1],data_vector[0][0][1][1],round(cosine_sim(datset1,dataset2),4))

                    generate_tuple.append([weeks,model,data_vector[0][1],data_vector[0][0][1][1],round(cosine_sim(datset1,dataset2),4)])
        #             print()
        #             print(weeks,model,cosine_sim(datset1,dataset2))
                except:
#                     print(weeks)
                    a.add(weeks)

                    pass
    #                 print(weeks,model,dataset2)
        state_dict[weeks] = week_dict

    State_Week_Model_name_Cosine_match_cases[State_name] = state_dict

    Model_actual_cosine_Agrremen_df = pd.DataFrame(generate_tuple)


    Model_actual_cosine_Agrremen_df.columns = ['Week Number',"Model Name","Predicted Label","True Label","Cosine Similarty"]
    
    Model_actual_cosine_Agrremen_df['State'] = State_name

    Master_df_actual_VS_Model_Agrrement = pd.concat([Master_df_actual_VS_Model_Agrrement,Model_actual_cosine_Agrremen_df],axis=0)
    

Master_df_actual_VS_Model_Agrrement.to_csv(Ouput_path+"Shapelet_model_evaluation_cases_cosine_modelVS_Actual.csv")

Master_df_actual_VS_Model_Agrrement


MeanSimilarityModels_Actual = Master_df_actual_VS_Model_Agrrement.groupby(['State','Week Number']).agg(Mean_Similarity=("Cosine Similarty","mean")).reset_index()



best_model_label_df = Master_df_actual_VS_Model_Agrrement.groupby(['True Label','Model Name']).agg(Mean_Score=("Cosine Similarty","mean")).reset_index()


#%% Agreement: NC2 conbinations for checking agreement between models

State_model_Week_vector_shapelet_Actual_dict.keys()

Master_df_Model_VS_Model_Agrrement = pd.DataFrame()

for State_name in State_model_Week_vector_shapelet_Actual_dict.keys():
    if State_name in Ignore_State_list:
        continue



    State_Week_Model_name_Cosine_match_cases = {}
    # State_name = 'California'



    # California_debug_actual = Shapelet_dict_actual_state_week_vector_label[State_name]

    California_debug_model =  State_model_Week_vector_shapelet_Actual_dict[State_name]


    generate_tuple = []

    state_dict = State_Week_Model_name_Cosine_match_cases.get(State_name,{})


    for weeks, model_level in California_debug_model.items():
#         if weeks>585:
#             continue
        week_dict = state_dict.get(weeks,{})
        
        

        for model1,data_vector1 in model_level.items():
            for model2,data_vector2 in model_level.items():
                
            
    #         print(data_vector)
                datset1 = data_vector1[0][0][0]
                dataset2 = data_vector2[0][0][1][0]
    #             model_val = week_dict.get(model,None)
    #             if model_val is None:
        #             try:
    #             week_dict[model] =(data_vector[0][1],data_vector[0][0][1][1],round(cosine_sim(datset1,dataset2),4))
                try:
                    if dataset2 is not None:
                        if datset1 is not None:
                            if model1!=model2:

                                if model1>model2:
                                    generate_tuple.append([weeks,model1,model2,round(cosine_sim(datset1,dataset2),4)])
                                else:
                                    generate_tuple.append([weeks,model2,model1,round(cosine_sim(datset1,dataset2),4)])
                except:
                    print([weeks,model2,model1,datset1,dataset2])
        #             print()
        #             print(weeks,model,cosine_sim(datset1,dataset2))
    #             except:

    #                 pass
    #                 print(weeks,model,dataset2)
#         state_dict[weeks] = week_dict

#     State_Week_Model_name_Cosine_match_cases[State_name] = state_dict

    Model_actual_cosine_Agrremen_df = pd.DataFrame(generate_tuple)


    Model_actual_cosine_Agrremen_df.columns = ['Week Number',"Model Name1","Model Name2","Cosine Similarty"]
    
    Model_actual_cosine_Agrremen_df['State'] = State_name

    Master_df_Model_VS_Model_Agrrement = pd.concat([Master_df_Model_VS_Model_Agrrement,Model_actual_cosine_Agrremen_df],axis=0)
    

Master_df_Model_VS_Model_Agrrement = Master_df_Model_VS_Model_Agrrement.drop_duplicates()

# Master_df_Model_VS_Model_Agrrement.shape


MeanSimilarityModels = Master_df_Model_VS_Model_Agrrement.groupby(['State','Week Number']).agg(Mean_Similarity=("Cosine Similarty","mean")).reset_index()


MeanSimilarityModels.to_csv(Ouput_path+"MeanSimilarity_within_models_cases.csv")

# len(MeanSimilarityModels)

## Ensemble Model Generation using mean pearson Vector



State_list_plotting = [w for w in list(Master_df_actual_VS_Model_Agrrement.State.unique()) if w not in Ignore_State_list]

State_week_avg_ensemble = {}
for state in State_list_plotting:
    Week_averge_cosine = {}

    for key, vale in State_model_Week_vector_shapelet_Actual_dict[state].items():
        vec1 = []
    #     actual_vec = []

        for k1,v1 in vale.items():
    #         print(v1)
    #         print(v1[0][0][0])
            vec1.append(v1[0][0][0])
            actual_vec = v1[0][0][1][0]
        denom = len(vec1)
        summation_list = []
        for i in range(Number_of_shapelets):
            avg_shape_cosin = (sum([w[i] for w in vec1]))/denom
            summation_list.append(avg_shape_cosin)
#         a = (sum([w[0] for w in vec1]))/denom
#         b = (sum([w[1] for w in vec1]))/denom
#         c=(sum([w[2] for w in vec1]))/denom
#         d=(sum([w[3] for w in vec1]))/denom
#         e=(sum([w[4] for w in vec1]))/denom
#         f=(sum([w[5] for w in vec1]))/denom
        try:
            Week_averge_cosine[key] = cosine_sim(actual_vec,summation_list)
        except:
            print(key)
    State_week_avg_ensemble[state] =Week_averge_cosine 


    
Master_df_actual_VS_Model_Agrrement.to_csv(Ouput_path+"Master_df_actual_VS_Model_Agrrement.csv")


Master_df_actual_VS_Model_Agrrement_1 = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State'].isin(State_list_plotting)]


Master_df_actual_VS_Model_Agrrement_2 = Master_df_actual_VS_Model_Agrrement_1.groupby(['State','Model Name']).agg(Mean_Similarity=("Cosine Similarty","mean"),Count_Similarity=("Cosine Similarty","count")).reset_index()


Master_df_actual_VS_Model_Agrrement_2


Master_df_actual_VS_Model_Agrrement_2["rank"] = Master_df_actual_VS_Model_Agrrement_2.groupby(["State"])["Mean_Similarity"].rank("dense", ascending=False)


Master_df_actual_VS_Model_Agrrement_2.sort_values(['rank']).to_csv(Ouput_path+"Model Ranking For Selected_States.csv")

df_top3_models_per_state = Master_df_actual_VS_Model_Agrrement_2[Master_df_actual_VS_Model_Agrrement_2['rank']<4]

Master_df_actual_VS_Model_Agrrement_2.sort_values(['rank','State']).head(5)

df2 = df_top3_models_per_state.groupby('State')['Model Name'].apply(list)

model_list = df2.to_dict()

for key,vale in model_list.items():
    print("For the State {} Top 3 performing Models are --> {}".format(key,str(vale)[1:-1])) 
    
    
subset = Master_df_actual_VS_Model_Agrrement[Master_df_actual_VS_Model_Agrrement['State']==state]
subset_1 = subset[subset['Model Name']==model_list[state][0]]



best_model_label_df = Master_df_actual_VS_Model_Agrrement.groupby(['True Label','Model Name']).agg(Mean_Score=("Cosine Similarty","mean")).reset_index()


best_model_label_df["rank"] = best_model_label_df.groupby(['True Label'])["Mean_Score"].rank("dense", ascending=False)


best_model_label_df.sort_values(['True Label','rank']).to_csv(Ouput_path+"Best_model_shapelet_6.csv")

Master_df_actual_VS_Model_Agrrement['True Label'].unique()


Master_df_actual_VS_Model_Agrrement['newlable'] = np.where(Master_df_actual_VS_Model_Agrrement['True Label'].isin(['Flat', 'Inc', 'Dec']),"Continued Trend","Others")


Master_df_actual_VS_Model_Agrrement


best_model_label_df = Master_df_actual_VS_Model_Agrrement.groupby(['newlable','Model Name']).agg(Mean_Score=("Cosine Similarty","mean")).reset_index()

best_model_label_df["rank"] = best_model_label_df.groupby(['newlable'])["Mean_Score"].rank("dense", ascending=False)



best_model_label_df.sort_values(['newlable','rank']).to_csv(Ouput_path+"Best_model_shapelet_continued_trendVS_others.csv")


