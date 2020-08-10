# csci499std: Predicting the county-level prevalence of Chlamydia in the United States

* data: Raw data for census values, chlamydia stats, and migration; FIPs county information; county adjacency information. To prepare the data frames before running the models, run prepare_dfs.py. Resulting data frames are stored in the prepared_data directory. 
* models: Code to develop linear regression, gradient boost, and random forest models with and without feature selection. The code for these models access the data frames in the ./data/prepared_data directory, which are then used to create data frames in ./data/prepared_data/all_features_dfs directory.
    * Linear regression: feature_selection_linreg_all_data.py
    * GBR: feature_selection_gbr_all_data.py
    * RF: feature_selection_rf_all_data.py
	Each of these files performs 5-fold cross validation, finds average r^2, average MSE, creates and saves plots for cross validation, finds the top 20 features, creates a model with only the top 20 features, and creates a plot with top 20 features.  
* figures: Map figures; figures for models with and without feature selection, organized by model type (linear regression, gradient boosting, random forest). 
* map_code: Code to generate various map figures
* optimization: Code for the optimization problem
