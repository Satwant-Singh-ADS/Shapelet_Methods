from configs import *

#### Used to convert numeric week to Date format basis logic of adding number to 22 Jan 2020
def date_formatting(week_nbr):
# week_nbr = 164
    t = 'Jan 22 2020'
    format = '%b %d %Y'
    now = datetime.strptime(t,format)
    after = now + timedelta(days = int(week_nbr))
    return after.date().strftime("%m/%d/%Y")

### based on underlying similzrity function, generates similatity matrix
def similarity_metrix(vector1,vector2):
    '''
    Here we have given user the flexibility to change the similarity function. Currently we have made it pearson correlation but it can be cosine
    
    1 - spatial.distance.cosine(vector1, vector2)
    '''
    similarity_value = pcor(vector1,vector2)[0][1]
    return similarity_value

### calculates score with all standard shapes and return standard shape with highlest similarity score
def return_best_shapelet_pearson(vector):
    correlation_lst = []
    corrs = []
    for i in range(len(shapelet_standard_array)):
        score = similarity_metrix(shapelet_standard_array[i],vector)
        correlation_lst.append(shapelet_standard_names[i])
        corrs.append(score)
    scenario = corrs.index(max(corrs))
    return correlation_lst[scenario]

### generate similairty score vector for all standard shapes compared with inpyt vector    
def return_all_shapelet_pearson(vector):
#     correlation_lst = []
    corrs = []
    for i in range(len(shapelet_standard_array)):
        score = similarity_metrix(shapelet_standard_array[i],vector)
#         correlation_lst.append(shapelet_standard_names[i])
        corrs.append(score)
    return corrs


def cosine_sim(dataSetI,dataSetII):
    return 1 - spatial.distance.cosine(dataSetI, dataSetII)

### function to sort data frame columns in increasing number of week nbr
def sort_df_name(df_master1):
    df_master = df_master1.reset_index()
    week_names = [int(w) for w in list(df_master.columns[1:-1])]
    week_names.sort()
    cols= ['State']
    cols.extend(week_names)
    return df_master[cols]
