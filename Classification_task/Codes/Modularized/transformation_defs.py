from configs_basic import *

### Helper function for computing our transformation 
#For shapelets that are not flat, we first compute correlation
#of the given shape with the shapelet. Operation is commutative
def similarity_non_flat(vector1,vector2):   
    if np.std(vector1) < 1e-100 or np.std(vector2) < 1e-100:
        similarity_value = 0
    else:
        similarity_value = pcor(vector1,vector2)[0][1]
    return similarity_value

### returns the shapelet name corresponding to the dimension with the 
# the highest value in the shapelet space representation
def return_best_shapelet(vector, slope_thres = 0.0005):
    corrs = return_all_shapelet_pearson(vector, slope_thres)
    scenario = corrs.index(max(corrs))
    return shapelet_names[scenario]

### generate shapelet space representation for the given vector
def shapelet_space_representation(vector, slope_thres = 0.0005):

    coords = []
    # The average absolute slope of slope_thres 
    # gets a flatness of 0.1. Modify below to change
    beta = -log(0.1)/slope_thres
    
    # flat threshold is m0. If the slope is below m0 flatness is 1
    m0 = 0
    slope =mean(abs(diff(vector)))
    if slope < m0:
        flatnes = 1
    else: 
        flatness = exp(-beta*(slope - m0));
    for i in range(len(shapelet_array)):
        if not(any(shapelet_array[i])):
            score = 2*flatness - 1
        else:
            score = (1-flatness)*similarity_non_flat(shapelet_array[i],vector)
        coords.append(score)
    return coords


### Cosine similarity is used to measure performance, agreement
def cosine_sim(coords1, coords2):
    return 1 - spatial.distance.cosine(coords1,coords2)

### Takes a time-series and finds the shapelet space representations
# with a rolling window. The output is a multi-variate time-series
# of the same length encoding the shapes in the time-series. 
def find_shapelet_space_ts(time_series, slope_thres = 0.0005):
    reps = [[0.0]*(len(time_series)-Shapelet_length+1)]*len(shapelet_names)
    reps = np.array(reps)
    for i in range(0,len(time_series)-Shapelet_length+1):
        this_shape = time_series[i:i+Shapelet_length]
        this_rep = shapelet_space_representation(this_shape, slope_thres)
        reps[:, i] = this_rep
    return reps    

