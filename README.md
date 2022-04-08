## Shape-based Evaluation of Epidemic Forecasts

## Definitions

Shapelet : Shapelets are defined as “subsequences that are in some sense maximally representative of a class”. Informally, if we assume a binary classification setting, a shapelet is discriminant if it is present in most series of one class and absent from series of the other class.<br>

In this work, we have used 6 shapelets which depict various stages in a pandemic wave

__Flat__: [1, 1, 1, 1, 1] <br>
__Stable-inc__: [1 ,2, 3, 4, 5], i.e., linear<br>
__Stable-dec__: [5, 4, 3, 2, 1], i.e., linear but decreasing<br>
__Surge__: [exp(-1/2) ,exp(0/2), exp(1/2), exp(2/2), exp(3/2)], i.e., like exp(x)<br>
__Peaking__: - [exp(1/2) ,exp(0/2) ,exp(-1/2) ,exp(-2/2), exp(-3/2)], i.e., like -exp(-x)<br>
__At/near peak__:  - [exp(-1/2), exp(0/2), exp(1/2), exp(2/2), exp(3/2)], i.e., like -exp(x)


## Broard Steps

For Cases and Deaths,

* Find the similarity of the ground truth with our shapelets. This will give us a vector
* Find the similarity of the model forecasts with our shapelets. This will give us another vector
* Take the cosine similarity between the two (negative inputs are okay!). The similarity between the classes will be inherently captured
* Take the mean of pairwise cosine similarity between the models. This will give us the agreement between models
*Add another "Shapelet Ensemble Model" whose vector output is the mean of the model vectors. This is analogous to the majority classifier.
 
