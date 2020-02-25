# csci499std

### Important files ###

* prepare_dfs.py: Creates data frame for all variables (STD, census, infected_inflow based off migration data). Saves data as pickle and Excel. 
    * Pickled data goes into these files: save_adj_fips_dict.p, save_census_dfs.p, save_fips_to_county_dict.p, save_migration_dfs.p, save_std_dfs.p
    * Data goes into these Excel files: full_features_by_year.xlsx, full_features_mig_no_nan_v.xlsx

* read_data.py: Class for reading in census data, std data, migration data (raw numbers), and county/neighbors dictionary.

* Models (linear regression, gradient boosting regressor, and random forest) are in feature_selection_all_features folder.

* Optimization files:
    * illinois_data
    * new_jersey
    * optimization_data

* Raw data is contained in census_data, chlam_data, migration_data

-----------------------------------------------------------------------

* std_county_map.py: Constructs maps of STD rates over the years.