## Shape-based Evaluation of Epidemic Forecasts

## Paper Link
https://arxiv.org/pdf/2209.04035.pdf

## Definitions

Shapelet : We define a shapelet as a vector that describes one of the shapes of interest in the trend of an epidemic. <br>

Shapelet Space: A set of shapelets that cover all shapes of interest.<br>
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
 

## Important instructions for smoothly running the process

Mainly there are 2 folders
1) Codes
2) Data Sources

### 1) Codes ->

### Details of Modular Folder

1) imports.py : It contains list of all the libraries used in the code
2) configs.py : There are several hyperparameters which are used in the process. To tweak them, user simply needs to make changes in config file. For example, I want to run process for California, I can make changes in config file and so on. Each hyper parameter in cofnig file is explained in detail in config file

3) Similarity_fxns.py : Currently we are making use of certain user defined functions while calculating similarity scores, for introducing new methods, make changes in this file

4)preprocessing.py : All the data preprocessing, data wrangling and manipulations are performed in this file.

5)modular_main.ipynb : This is the man code which calls all the other python codes and is used by end user for generating visualizations and other analysis.

6)Covid_WBench_gen.ipynb : This code is used to generate evaluation files for Covid-WorkBench UI.


### 2) Data Sources ->
Now lets talk about Data_Sources Folder.

We have two forecasts, 1 for cases, 1 for deaths. Since we want to ensure modularity, dedicated folder structure is used for eachof them.

1) Cases --> Here all the model input files, visualization results, output csv files, intermediate pickle files are stored.
2) Deaths --> Here all the model input files, visualization results, output csv files, intermediate pickle files are stored.
3) Evaluation --> Here Evaluation files for covid19 work bench are stored



### ########## Major Input Sources ###############################

1) Covid-19 Actual Incidence file. It is coming from a github repo. I have made a local copy but to use a latest version, refer github link.

Cases : Classification_task/Data_Sources/Cases/Input_Files/Actual_Incidence_Data/US_actual_data.csv
Deaths : Classification_task/Data_Sources/Deaths/Input_Files/Actual_Incidence_Data/US_actual_data.csv

2) Model Forecasts Data: Models generate case/death forecasts every week. Prof has a ssc github repo where he stores processed forecast files. 
Classification_task/Data_Sources/Cases/Input_Files/Model_Forecasts_Data/US-COVID/state-case
Update this folder for latest results.
https://github.com/scc-usc/covid19-forecast-bench/tree/master/formatted-forecasts/US-COVID/state-case



Github Page for this Project
https://github.com/Satwant-Singh-ADS/Shapelet_Methods/

Run modular_main.py & preprocessing.py in Modular Folder and to generate all the results used in our IEEE BigData 2022 paper
