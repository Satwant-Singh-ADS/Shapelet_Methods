## Shape-based Evaluation of Epidemic Forecasts

## Definitions

Shapelet : We define a shapelet as a vector that describes one of the shapes of interest in the trend of an epidemic. <br>

Shapelet Space: A set of shapelets that cover all shapes of interest.
__Stable-inc__: [1 ,2, 3, 4, 5], i.e., linear<br>
__Stable-dec__: [5, 4, 3, 2, 1], i.e., linear but decreasing<br>
__Surge__: [exp(-1/2) ,exp(0/2), exp(1/2), exp(2/2), exp(3/2)], i.e., like exp(x)<br>
__Peaking__: - [exp(1/2) ,exp(0/2) ,exp(-1/2) ,exp(-2/2), exp(-3/2)], i.e., like -exp(-x)<br>
__At/near peak__:  - [exp(-1/2), exp(0/2), exp(1/2), exp(2/2), exp(3/2)], i.e., like -exp(x) <br>
__Flat__: [1, 0, 1, 0, 1] (intended to be a constant, but implemented this way to allow computing correlation) <br>

## Broard Steps

For Cases and Deaths,

* Find the similarity (currently implemented as Pearson correlation) of the ground truth with the set of shapelets. This will result in the feature space representation of the observed shape in the "shapelet space"
* Find the similarity of the model forecasts with the set of shapelets. This will result in the feature space representation of the predicted shape in the "shapelet space"
* Performance: Cosine similarity between the shapelet space representations of forecasts and ground truth
* Agreement: Mean pairwise cosine similarity of shapelet space representation of forecasts
* This code also adds a "Shapelet Ensemble Model" which is the mean of the shapelet representation of all forecasts
 

