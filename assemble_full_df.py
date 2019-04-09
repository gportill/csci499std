import read_data
import pandas as pd

# for a particular year
    # for each row of STD data: => county i (for each row, we will look at county i's neighbors in migration data)
        # store the county's neighbors in a list (available in adj_fips_dict)
        # initialize expected_infected = 0
        # for each neighbor j in the list:
            # find neighbor j's migration rate to county i in mig_dfs for this year
            # find neighbor j's total pop in census data for this year
            # find neighbor's std cases in std data for this year
            # expected_infected = calculate std_cases / total_pop * mig_rate
            # add that calculation to the expected_infected variable (so you are adding up expected_infected for all of their neighbors). this number will be the feature in the end.

cols_to_keep = {"Geo_FIPS": "fips",
                "SE_A00001_001": "total_pop",
                "SE_A00002_001": "pop_density",
                "SE_A02001_002": "male",
                "SE_A02001_003": "female",
                "SE_A01001_002": "age_under5",
                "SE_A01001_003": "age_5_to_9",
                "SE_A01001_004": "age_10_to_14",
                "SE_A01001_005": "age_15_to_17",
                "SE_A01001_006": "age_18_to_24",
                "SE_A01001_007": "age_25_to_34",
                "SE_A01001_008": "age_35_to_44",
                "SE_A01001_009": "age_45_to_54",
                "SE_A01001_010": "age_55_to_64",
                "SE_A01001_011": "age_65_to_74",
                "SE_A01001_012": "age_75_to_84",
                "SE_A01001_013": "age_85older",
                "SE_A03001_002": "race_white_alone",
                "SE_A03001_003": "race_black",
                "SE_A03001_004": "race_american_indian_alaska_native_alone",
                "SE_A03001_005": "race_asian_alone",
                "SE_A03001_006": "race_native_hawaiian",
                "SE_A03001_007": "race_other_race_alone",
                "SE_A03001_008": "race_two_races",
                "SE_A04001_002": "not_hispanic_total",
                "SE_A04001_003": "not_hispanic_white_alone",
                "SE_A04001_004": "not_hispanic_black",
                "SE_A04001_005": "not_hispanic_american_indian",
                "SE_A04001_006": "not_hispanic_asian_alone",
                "SE_A04001_007": "not_hispanic_native_hawaiian",
                "SE_A04001_008": "not_hispanic_other_race_alone",
                "SE_A04001_009": "not_hispanic_two_races",
                "SE_A04001_010": "hispanic_total",
                "SE_A04001_011": "hispanic_white_alone",
                "SE_A04001_012": "hispanic_black",
                "SE_A04001_013": "hispanic_american_indian",
                "SE_A04001_014": "hispanic_asian_alone",
                "SE_A04001_015": "hispanic_native_hawaiian",
                "SE_A04001_016": "hispanic_other_race_alone",
                "SE_A04001_017": "hispanic_two_races",
                "SE_A10003_001": "avg_household_size",
                "SE_A11001_001": "pop_15_and_older",
                "SE_A11001_002": "never_married",
                "SE_A11001_003": "now_married",
                "SE_A11001_004": "separated",
                "SE_A11001_005": "widowed",
                "SE_A11001_006": "divorced",
                "SE_A12002_002": "edu_attainment_less_than_high_school",
                "SE_A12002_003": "edu_attainment_high_school_grad",
                "SE_A12002_004": "edu_attainment_some_college",
                "SE_A12002_005": "edu_attainment_bach_degree",
                "SE_A12002_006": "edu_attainment_masters_degree",
                "SE_A12002_007": "edu_attainment_professional_school_degree",
                "SE_A12002_008": "edu_attainment_doctorate_degree",
                "SE_A12003_002": "school_dropout_16_to_19_not_hs_graduate",
                "SE_A12003_003": "school_dropout_hs_graduate",
                "SE_A17002_002": "employment_status_16_plus_IN_labor_force",
                "SE_A17002_003": "employment_status_16_plus_in_armed_forces",
                "SE_A17002_004": "employment_status_16_plus_civilian",
                "SE_A17002_005": "employment_status_16_plus_civilian_employed",
                "SE_A17002_006": "employment_status_16_plus_civilian_unemployed",
                "SE_A17002_007": "employment_status_16_plus_not_in_labor_force",
                "SE_A17005_002": "employment_rate",
                "SE_A17005_003": "unemployment_rate",
                "SE_A14001_002": "household_income_less_than_10000",
                "SE_A14001_003": "household_income_10_to_15",
                "SE_A14001_004": "household_income_15_to_20",
                "SE_A14001_005": "household_income_20_to_25",
                "SE_A14001_006": "household_income_25_to_30",
                "SE_A14001_007": "household_income_30_to_35",
                "SE_A14001_008": "household_income_35_to_40",
                "SE_A14001_009": "household_income_40_to_45",
                "SE_A14001_010": "household_income_45_to_50",
                "SE_A14001_011": "household_income_50_to_60",
                "SE_A14001_012": "household_income_60_to_75",
                "SE_A14001_013": "household_income_75_to_100",
                "SE_A14001_014": "household_income_100_to_125",
                "SE_A14001_015": "household_income_125_to_140",
                "SE_A14001_016": "household_income_150_to_200",
                "SE_A14001_017": "household_income_over_200",
                "SE_A13002_002": "poverty_status_12mo_families_with_income_below_poverty_level",
                "SE_A13002_003": "poverty_status_12mo_family_type_married_with_children",
                "SE_A13002_004": "poverty_status_12mo_family_type_married_no_children",
                "SE_A13002_006": "poverty_status_12mo_family_type_malehouseholder_nowife_with_children",
                "SE_A13002_007": "poverty_status_12mo_family_type_malehouseholder_nowife_no_children",
                "SE_A13002_009": "poverty_status_12mo_family_type_femalehouseholder_nohusband_with_children",
                "SE_A13002_010": "poverty_status_12mo_family_type_num_",
                "SE_A13002_011": "poverty_status_12mo_family_type_num",
                "SE_A13003A_002": "poverty_status_under18_living_in_poverty",
                "SE_A13003B_002": "poverty_status_18_to_64_living_in_poverty",
                "SE_A13003C_002": "poverty_status_65older_living_in_poverty",
                "SE_A13001A_002": "poverty_status_white_alone_below_poverty_level",
                "SE_A13001B_002": "poverty_status_black_alone_below_poverty_level"}

cols_to_keep_list = list(cols_to_keep.keys())

rd = read_data.ReadData()
print("reading read_std_data")
std_dfs = rd.read_std_data()
print("reading adj_fips_dict")
adj_fips_dict = rd.read_county_neighbors()
print("reading census_data")
census_dfs = rd.read_census_data()




# -------------------------------------
fips_to_county_dict = rd.get_fips_to_county_dict()
col_data = [[] for i in range(95)]  # array of empty lists.
# index 0 is year
# indices 1 to 94 are census data
# index 95 is std cases
# index 96 is infected_inflow

for i in range(2006, 2017):
    year = str(i)
    census_df = census_dfs[year]

    # loop over rows in this year's census data
    for idx, val in census_df.iterrows():
        fips = census_df["Geo_FIPS"][idx]
        if fips in fips_to_county_dict.keys():  # skip any counties whose FIPS are not in fips_to_county_dict
            county = fips_to_county_dict[fips]  # county is a county object
        else:
            continue

        col_data[0].append(i)  # set year for this row

        # adding census data for all the census columns we want to keep
        for k in range(0, len(cols_to_keep_list)):
            curr_column = cols_to_keep_list[k]
            value = census_df[curr_column][idx]
            col_data[k+1].append(value)
            # print(cols_to_keep_list[k])

        # now columns 0 and 1-94 are filled

        # add cases info
        cases = county.year_to_cases_dict[year]
        col_data[94].append(cases)

        # add infected_inflow data
        # inflow_df = year_to_county_to_STD_inflows[year]
        # col_data[96].append(inflow_df[county.fips])

census_col_names = census_dfs["2006"].columns
descriptive_census_col_names = []
for i in range(0, len(census_col_names)):
    descriptive_census_col_names.append(cols_to_keep[census_col_names[i]])

column_names = ['year']
for i in range(0, len(descriptive_census_col_names)):
    column_names.append(descriptive_census_col_names[i])
column_names.append('rate')
# column_names.append('infected_inflow')

data_with_col_names = dict(zip(column_names, col_data))
full_df = pd.DataFrame(data_with_col_names)

# column_names is header
# col_data has all the information, one list per column
full_df_no_na = full_df.copy()
full_df_no_na = full_df_no_na.dropna(axis='columns', how='any')

full_df.to_excel("full_features_no_mig1.xlsx", na_rep="nan", index=False)
full_df_no_na.to_excel("full_features_no_mig_NO_NAN1.xlsx", na_rep="nan", index=False)

# -------------------------------------

''' # Notes from Aaron
full_df.describe()
full_df.to_pickle

# store full_df as pickle or excel
#
train_years = [2006, ...]
test_years = [2013, ...]
feature_columns = full_df.columns

full_df[feature_columns].as_matrix()
# linear reression
# gradient boosted ensemble
# multilayer perceptron

'''
