from imports import *

vector_length = (0,4)
## (0,4) means look 4 weeks ahead in future while defining shapelet
## (1,4) means look 4 weeks ahead in future, 1 week in past basically N-1 week from actual covid incidence list for defining shapelet
## For COVID-19 forecasting evaluation 4 week ahead would be the upper limit as models typical do not submit beyond 4 weeks

history_weeks = vector_length[0]
future_weeks = vector_length[1]


# Hyper Params 

Number_of_shapelets = 6 ### 6 

global Shapelet_length
Shapelet_length = vector_length[0]+vector_length[1]

shapelet_array = [[0]*Shapelet_length for w in range(Number_of_shapelets)]
## here we have initialized an zero valued array of array.

shapelet_names = ["Flat","Inc",'Dec',"Surge",'Past Peak',"Near Peak"]
# shapelet_names = ["Flat","Inc",'Dec',"Surge","Peak"]

shapelet_array[0] = [0,0,0,0] # flat
shapelet_array[1] = [1,2,3,4] # inc
shapelet_array[2] = [4,3,2,1] # dec

## Could also use the following definitions of curved shapelets
# shapelet_array[3] = [1,2,4,8] # surge
# shapelet_array[4] = [-1,-2,-4,-8] # past peak
# shapelet_array[5] = [-1,-0.5,-0.25,0.125] # near peak

shapelet_array[3] = [exp(-2), exp(0), exp(2), exp(4)] # surge
shapelet_array[4] = [-exp(-2), -exp(0), -exp(2), -exp(4)] # past peak
shapelet_array[5] = [-1/exp(-2), -1/exp(0), -1/exp(2), -1/exp(4)] # near peak

# shapelet_array[3] = [exp(-2), exp(0), exp(2), exp(4)]
# shapelet_array[4] = [1,2,2,1]

assert len(shapelet_array[0])==Shapelet_length, 'Size of defined shapelet array mismatch for shapelet_names and value of  Shapelet_length.please check vector_length'
assert len(shapelet_names)==Number_of_shapelets, 'Size of array mismatch for shapelet_names and value of  Number_of_shapelets'
