from imports import *

Runtype = "Flu"#### 2 values Cases and Deaths. choose Deaths for generating results for deaths and Cases for generating case results
qualifying_threshold = 10
### basically not all models should be part of the analysis. we want to use only those models which made submissions beyond a certain number of weeks. Currently set to 60 weeks. you can change that 
Evaluation_files_github ='../../Data_Sources/Evaluation/'
if Runtype =='Cases':
    print("Process will run for Cases")
    Input_path = '../../Data_Sources/Cases/'
    Ouput_path = '../../Data_Sources/Cases/Output_Files/'
    root_tmp = glob.glob(Input_path+"Input_Files/Model_Forecasts_Data/US-COVID/state-case/*")
     
elif Runtype == 'Deaths':
    print("Process will run for Deaths")
    Input_path = '../../Data_Sources/Deaths/'
    Ouput_path = '../../Data_Sources/Deaths/Output_Files/'
    root_tmp = glob.glob(Input_path+"Input_Files/Model_Forecasts_Data/US-COVID/state-death/*")

else:
    Input_path = '../../Data_Sources/Flu-2023/'
    Ouput_path = '../../Data_Sources/Flu-2023/Output_Files/'
    root_tmp = glob.glob(Input_path+"Input_Files/Model_Forecasts_Data/US-Flu/*")


Actual_incidence_path = Input_path+"Input_Files/Actual_Incidence_Data/"
pickle_path = Input_path+"Pickle_Objects/"
Visualization_path = Input_path+"Visualizations/"





export_visualizations = False ### when this is set to True, visualizations will be expored. If False, visualizations will only be displayed not exported
Data_refresh = 1   ### we use Model forecasts data. each model each week csv file with 4 weeks ahead predictions. If our data has not refreshed from last run, we should skip this preprocessing step of loading csvf iles . then we use a pickle file with all preprocessing done.  

### if it is set to 1, data processing of all models needs to be done. As is this needs to be set1 when we feel model data need to be updated else 0


#### Ignore model List 
Ignore_model_list  = []

Ignore_State_list = []

# Ignore_State_list = ['Illinois', 'Arizona', 'Massachusetts',
#        'Wisconsin', 'Texas', 'Nebraska', 'Utah', 'Oregon','United States','Washington',
#        'New York', 'Rhode Island', 'Georgia', 'New Hampshire',
#        'North Carolina', 'New Jersey', 'Colorado', 'Maryland', 'Nevada',
#        'Tennessee', 'Hawaii', 'Indiana', 'Kentucky', 'Minnesota',
#        'Oklahoma', 'Pennsylvania', 'South Carolina',
#        'District of Columbia', 'Kansas', 'Missouri', 'Vermont',
#        'Virginia', 'Connecticut', 'Iowa', 'Louisiana', 'Ohio', 'Michigan',
#        'South Dakota', 'Arkansas', 'Delaware', 'Mississippi',
#        'New Mexico', 'North Dakota', 'Wyoming', 'Alaska', 'Maine',
#        'Alabama', 'Idaho', 'Montana', 'Puerto Rico', 'Virgin Islands',
#        'Guam', 'West Virginia', 'Northern Mariana Islands',
#        'American Samoa']

# select_state_list = ["Florida"]

# State_list = ["Florida"]


vector_length = (0,4)   ### 1 means using N-1 week value for defining shapelet and 4 weeks 4 weeks from future. 4 can't be changed because models generate only 4 weeks ahead predictions.
## (0,4) means look 4 weeks ahead in future while defining shapelet
## (1,4) means look 4 weeks ahead in future, 1 week in past basically N-1 week from actual covid incidence list for defining shapelet

history_weeks = vector_length[0]

future_weeks = vector_length[1]

assert future_weeks<=4,"Looking 4 weeks in future is fixed because our modelsgenerate 4 weeks ahead predictions. \n Please change vector_length[1]"


# Hyper Params 

Number_of_shapelets = 4 ### 6 

global Shapelet_length
Shapelet_length = vector_length[0]+vector_length[1]

shapelet_standard_array = [[0]*Shapelet_length for w in range(Number_of_shapelets)]
## here we have initialized an zero valued array of array.

#shapelet_standard_names = ["Flat","Inc",'Dec',"Surge",'Past Peak',"Near Peak"]
shapelet_standard_names = ["Flat","Inc",'Dec',"Peak"]

assert len(shapelet_standard_names)==Number_of_shapelets, 'Size of array mismatch for shapelet_standard_names and value of  Number_of_shapelets'


shapelet_standard_array[0] = [0,0,0,0]
shapelet_standard_array[1] = [1,2,3,4]
shapelet_standard_array[2] = [4,3,2,1]

# shapelet_standard_array[3] = [1,2,4,8]
# shapelet_standard_array[4] = [-1,-2,-4,-8]
# shapelet_standard_array[5] = [-1,-0.5,-0.25,0.125]

# shapelet_standard_array[3] = [exp(-2), exp(0), exp(2), exp(4)]
# shapelet_standard_array[4] = [-exp(-2), -exp(0), -exp(2), -exp(4)]
# shapelet_standard_array[5] = [-1/exp(-2), -1/exp(0), -1/exp(2), -1/exp(4)]

# shapelet_standard_array[3] = [exp(-2), exp(0), exp(2), exp(4)]
shapelet_standard_array[3] = [1,2,2,1]

assert len(shapelet_standard_array[0])==Shapelet_length, 'Size of defined shapelet array mismatch for shapelet_standard_names and value of  Shapelet_length.please check vector_length'

