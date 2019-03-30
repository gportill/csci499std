import pandas as pd

census_files = ["./census_data/2006_census_with_total_pop.csv", "./census_data/2007_census_with_total_pop.csv", "./census_data/2008_census_with_total_pop.csv", "./census_data/2009_census_with_total_pop.csv", "./census_data/2010_census_with_total_pop.csv", "./census_data/2011_census_with_total_pop.csv", "./census_data/2012_census_with_total_pop.csv", "./census_data/2013_census_with_total_pop.csv", "./census_data/2014_census_with_total_pop.csv", "./census_data/2015_census_with_total_pop.csv", "./census_data/2016_census_with_total_pop.csv"]

census_dfs = {}

year = 2005

for file in census_files:
    year += 1
    # print(str(year))
    key = str(year)
    census_dfs[key] = pd.read_csv(file, encoding='latin-1', index_col=False)

# print(census_dfs["2006"].iloc[0,:])

# for year in range(2006, 2017):
#     year_str = str(year)
#     print("YEAR: " + year_str)
#     column_names = census_dfs[year_str].columns.values
#     for name in column_names:
#         print(name)
#     print()
#     print()
#     print()

# print(census_dfs["2006"].columns.values)
# print(census_dfs["2008"].columns.values)

# only difference between 2006 and 2008 is that 2008 has these additional:
# 'SE_A20001_001' 'SE_A20001_002' 'SE_A20001_003' 'SE_A20001_004' 'SE_A20001_005']
# health insurance?

# keep only the columns we need

# df1 = df[['a','d']]

# cols_to_keep = {"Geo_FIPS": "fips", "Geo_NAME": "county_name", "SE_A00001_001": "total_pop", "SE_A00002_001": "pop_density", "SE_A02001_001": "sex", "SE_A01001_001": "age", "SE_A03001_001": "race", "SE_A04001_001": "hispanic or latino by race", "SE_A10003_001": "avg_household_size", "SE_A11001_001": "martial_status", "SE_A12002_001": "highest_edu", "SE_A17002_001": "emp_status", "SE_A17005_001": "unemp_rate_total_pop", "SE_A14001_001": "household_inc", "SE_A10044_001": "occupancy_status", "SE_A13002_001": "pov_status_by_family_type", "SE_A13003A_001": "pov_status_under_18", "SE_A13003B_001": "pov_status_18_64", "SE_A13003C_001": "pov_status_65_plus", "SE_A13001A_001": "pov_white", "SE_A13001B_001": "pov_black", "SE_A13001C_001": "pov_american_indian", "SE_A13001D_001": "pov_asian_alone", "SE_A13001E_001": "pov_native_haiwaiian", "SE_A13001F_001": "pov_some_other_race_alone", "SE_A13001G_001": "pov_two_races", "SE_A13001H_001": "pov_hispanic_latino", "SE_A13001I_001": "pov_white_alone_not_hispanic_latino", "SE_A08001_001": "res_1_year_ago", "SE_A08002B_007": "geo_mobility"}
# "SE_A20001_001": "health_insurance"
# "SE_A10044_001": "occupancy_status", "SE_A13002_001": "pov_status_by_family_type",
cols_to_keep = {"Geo_FIPS": "fips", "Geo_NAME": "county_name", "SE_A00001_001": "total_pop", "SE_A00002_001": "pop_density",
                "SE_A02001_001": "sex", "SE_A01001_001": "age", "SE_A03001_001": "race", "SE_A04001_001": "hispanic or latino by race",
                "SE_A10003_001": "avg_household_size", "SE_A11001_001": "martial_status", "SE_A12002_001": "highest_edu",
                "SE_A17002_001": "emp_status", "SE_A17005_001": "unemp_rate_total_pop", "SE_A14001_001": "household_inc",
                "SE_A13003A_001": "pov_status_under_18", "SE_A13003B_001": "pov_status_18_64",
                "SE_A13003C_001": "pov_status_65_plus", "SE_A08001_001": "res_1_year_ago",
                "SE_A08002B_007": "geo_mobility"}

vars_to_code = {v: k for k, v in cols_to_keep.items()}

col_keys = list(cols_to_keep.keys())
print(col_keys)

census_dfs_cond = {}
for year in range(2006, 2017):
    year_str = str(year)
    curr_df = census_dfs[year_str]
    new_df = curr_df[col_keys]
    print(new_df.head(5))
    census_dfs_cond[year_str] = new_df

print(census_dfs_cond)
print(census_dfs_cond["2008"].columns.values)