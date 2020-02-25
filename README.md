# csci499std: Predicting the county-level prevalence of Chlamydia in the United States

* Models are in feature_selection_all_features folder
    * linear regression: feature_selection_linreg_all_data.py
    * gradient boosting regressor: feature_selection_gbr_all_data.py
    * random forest: feature_selection_rf_all_data.py
Each of these files performs 5-fold cross validation, finds average r^2, average MSE, creates and saves plots for cross validation, finds the top 20 features, creates a model with only the top 20 features, and creates a plot with top 20 features. 
Figures are saved to all_feature_figures folder. 

-----------------------------------------------------------------------

* Raw data is contained in census_data, chlam_data, migration_data

* all_feature_figures: contains the plots that are created by feature_selection_linreg_all_data.py, feature_selection_gbr_all_data.py, and feature_selection_rf_all_data.py
* all_feature_dfs: contains the data frames used by feature_selection_linreg_all_data.py, feature_selection_gbr_all_data.py, and feature_selection_rf_all_data.py
* census_data: raw data
* chlam_data: raw data for Chlamydia
* feature_selection_all_features: contains the final linear regression, GBR, and random forest models
* illinois_data:
* map_pics: maps of Chlamydia rates
* migration_data: raw data
* new_jersey: New Jersey data and cases per person for years 2006-2011 
* optimization_data: total number of cases for counties in New Jersey and Illinois 
* column_names_dict
* columns_to_keep
* county_adjacency: data about which counties neighbor a given county
* covered_counties_map: generate map of which counties the CDC provides STD data for
* fips_codes: data that associates FIPS codes to county names
* full_features_by_year: generated when prepare_dfs.py is run. A table with 11 sheets (one for each year) that has 43 features for each year. 
* full_features_mig_no_nan_v: generated when prepare_dfs.py is run. A table with a single sheet where all years of data are combined. Used to create time-independent linear regression model. 
* illinois_data_frames.py: builds data frames for Illinois optimization
* included_fips: FIPS codes that are included in STD data from CDC
* nj_optimization_data_2012_2016_cases_per_person: table of cases_per_person for years 2012-2016 for each Ne wJersey county (by FIPS code). 
* nj_predicted_data.py: predicts rates of STDs in New Jersey for next year
* nj_predictions_2011.xlsx: New Jersey FIPS code, total_population, cases_per_person, and predicted number of expected cases
* optimization: Gurobi optimization problem 
* optimization_std_data
* prepare_dfs.py: Creates data frame for all variables (STD, census, infected_inflow based off migration data). Saves data as pickle and Excel. 
    * Pickled data goes into these files: save_adj_fips_dict.p, save_census_dfs.p, save_fips_to_county_dict.p, save_migration_dfs.p, save_std_dfs.p
    * Data goes into these Excel files: full_features_by_year.xlsx, full_features_mig_no_nan_v.xlsx
* read_data.py: Class for reading in census data, std data, migration data (raw numbers), and county/neighbors dictionary.
* save_adj_fips_dict.p: created by prepare_dfs.py
* save_census_dfs.p: created by prepare_dfs.py
* save_fips_to_county_dict.p: created by prepare_dfs.py
* save_migration_dfs.p: created by prepare_dfs.py
* save_std_dfs.p: created by prepare_dfs.py
* std_clinic_data.xlsx.csv: coordinates and addrsses of STD clinics in Illinois
* std_clinics.py
* std_county_map.py: constructs maps of STD rates over the years.
