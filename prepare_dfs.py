import read_data
import pandas as pd
import pickle
from sklearn import preprocessing

# rename the census variables that will be kept
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

# ------ uncomment the first time you run it; comment it out for all the runs after ------
rd = read_data.ReadData()
print("reading read_std_data")
std_dfs = rd.read_std_data()
print("reading adj_fips_dict")
adj_fips_dict = rd.read_county_neighbors()
print("reading census_data")
census_dfs = rd.read_census_data()
print("reading migration data")
migration_dfs = rd.read_migration_data()
fips_to_county_dict = rd.get_fips_to_county_dict()

pickle.dump(std_dfs, open("save_std_dfs.p", "wb"))
pickle.dump(adj_fips_dict, open("save_adj_fips_dict.p", "wb"))
pickle.dump(census_dfs, open("save_census_dfs.p", "wb"))
pickle.dump(migration_dfs, open("save_migration_dfs.p", "wb"))
pickle.dump(fips_to_county_dict, open("save_fips_to_county_dict.p", "wb"))
# ------ end uncomment pickle section ------

std_dfs = pickle.load(open("save_std_dfs.p", "rb"))
adj_fips_dict = pickle.load(open("save_adj_fips_dict.p", "rb"))
census_dfs = pickle.load(open("save_census_dfs.p", "rb"))
migration_dfs = pickle.load(open("save_migration_dfs.p", "rb"))
fips_to_county_dict = pickle.load(open("save_fips_to_county_dict.p", "rb"))

# list of years in the data range
years = []
for i in range(2006, 2017):
    years.append(str(i))

# ------ feature engineering to estimate the number of people with an STD entering each county ------
# to determine the expected infected inflow of migrants:
    # for each year, for each county i, determine county i's neighbors
    # for each neighbor j, find j's migration rate to county i and find j's number of std_cases
    # expected_infected_from_j = std_cases_j / total_pop_j * mig_rate_from_j_to_i
    # county i's total expected_infected is the sum of expected_infected coming into county i for each neighbor j

year_to_county_to_STD_inflows = {}

for i in range(2006, 2017):
    mig_df = migration_dfs[str(i)]  # look up the migration data frame for this year
    mig_df.drop_duplicates(subset=["destination", "origin"],  keep='first', inplace=True)
    mig_df.set_index(["destination", "origin"], inplace=True)  # makes it a multi index

    std_df = std_dfs[str(i)].copy()  # std_df is the data frame of std data for this year
    std_df.set_index("Geography",inplace=True)

    census_df = census_dfs[str(i)].copy()  # census_df is the data frame of census data for this year
    census_df.set_index("Geo_FIPS",inplace=True)

    census_total_pop_column = 'SE_A00001_001'
    dest_to_inflow = {}
    # for each county
    for destination in fips_to_county_dict.keys():
        total_infected_inflow = 0
        # for each neighbor
        for origin in fips_to_county_dict[destination].neighbors:
            # calculate infected inflow from this neighbor
            # get cases of infection
            cases = '0'
            if origin in std_df.index:
                cases = std_df.loc[origin]["Cases"]
            # get the population
            pop = '0'
            if origin in census_df.index:
                pop = census_df.loc[origin][census_total_pop_column]
            # calculate ratio of cases to total population
            if float(pop.replace(",", "")) == 0:
                infected_ratio = 0
            else:
                infected_ratio = float(cases.replace(",", "")) / float(pop.replace(",", ""))

            # infected inflow = infected_ratio * num migrating to dest
            if (destination, origin) in mig_df.index:
                # num_exemps is number of migrants from county i to neighbor j
                num_exemps = float(mig_df.loc[destination, origin]["num_exemps"])

            infected_flow = infected_ratio * num_exemps
            total_infected_inflow += infected_flow  # sum up infected_inflow for all of i's neighbors

        # add total to dictionary
        dest_to_inflow[destination] = total_infected_inflow
    # add dictionary to dictionary
    year_to_county_to_STD_inflows[str(i)] = dest_to_inflow
# ------ end feature engineering for infected_inflow variable ------

# ------ combine all 98 variables into one data frame ------
col_data = [[] for i in range(98)]  # array of empty lists
# index 0 is year
# indices 1 to 93 are census data
# index 94 is std cases PER PERSON
# index 95 is infected_inflow
# index 96 is total cases in county
# index 97 is raw number of cases (not normalized)

counter = 0
for i in range(2006, 2017):
    print("start for " + str(i) + ": " + str(counter))
    year = str(i)
    census_df = census_dfs[year]

    # loop over rows in year i's census data
    for idx, val in census_df.iterrows():
        counter += 1
        fips = census_df["Geo_FIPS"][idx]
        if fips in fips_to_county_dict.keys():
            county = fips_to_county_dict[fips]  # county is a County object
        else:  # skip any counties whose FIPS are not in fips_to_county_dict
            continue

        col_data[0].append(i)  # set year for this row

        total_pop_val = 0

        # add census data for all the census columns we want to keep
        for k in range(0, len(cols_to_keep_list)):
            curr_column = cols_to_keep_list[k]
            value = census_df[curr_column][idx]
            if cols_to_keep[curr_column] == "total_pop":
                total_pop_val = value
            col_data[k+1].append(value)

        # now columns 0 and 1-93 are filled

        # add cases data
        if county.year_to_cases_dict[year] == 'Data not available':
            cases = 0
            cases_per_person = 0
        else:
            cases = float(county.year_to_cases_dict[year])
            cases_per_person = float(county.year_to_cases_dict[year]) / float(total_pop_val)
        col_data[94].append(cases_per_person)
        col_data[96].append(cases)
        col_data[97].append(cases)

        # add infected_inflow data
        inflow_df = year_to_county_to_STD_inflows[year]
        col_data[95].append(inflow_df[county.fips])

census_col_names = census_dfs["2006"].columns
descriptive_census_col_names = []
for i in range(0, len(census_col_names)):
    descriptive_census_col_names.append(cols_to_keep[census_col_names[i]])

column_names = ['year']
for i in range(0, len(descriptive_census_col_names)):
    column_names.append(descriptive_census_col_names[i])
column_names.append('cases_per_person')
column_names.append('infected_inflow')
column_names.append('cases')
column_names.append('cases_raw')

data_with_col_names = dict(zip(column_names, col_data))
full_df = pd.DataFrame(data_with_col_names)
# column_names is header
# col_data has all the information, one list per column
print("full_df before normalization")
print(full_df.head())
# ------ full_df now has all data for all years------

# ------ normalize all variables but fips, years, cases_per_person, and cases_raw ------
col_names_to_normalize = list(full_df.columns.values)

# remove variables that do not need to be normalized
col_names_to_normalize.remove('fips')
col_names_to_normalize.remove('year')
col_names_to_normalize.remove('cases_per_person')
col_names_to_normalize.remove('cases_raw')

min_max_scaler = preprocessing.MinMaxScaler()
x = full_df[col_names_to_normalize].values
x_scaled = min_max_scaler.fit_transform(x)
df_temp = pd.DataFrame(x_scaled, columns=col_names_to_normalize, index=full_df.index)
full_df[col_names_to_normalize] = df_temp
print("full_df after normalization")
print(full_df.head())
# ------ end normalization ------

# ------ remove NaN values from full_df ------
full_df.columns[full_df.isna().any()].tolist()

# create data frame without NaN values
full_df_no_na = full_df.copy()
full_df_no_na = full_df_no_na.dropna(axis='columns', how='any')
full_df_no_na.to_excel("full_features_mig_no_nan_v.xlsx", na_rep="nan", index=False)

# If you want all the data (with columns that contain NaN values), save full_df to an excel
# full_df.to_excel("full_features_mig_v.xlsx", na_rep="nan", index=False)
# ------ end remove NaN -------

# ------ create data frames for each year ------
year_dfs = {}
year_dfs[2006] = (full_df_no_na[:782])
year_dfs[2007] = (full_df_no_na[782:1569])
year_dfs[2008] = (full_df_no_na[1569:2358])
year_dfs[2009] = (full_df_no_na[2358:3149])
year_dfs[2010] = (full_df_no_na[3149:3955])
year_dfs[2011] = (full_df_no_na[3955:4765])
year_dfs[2012] = (full_df_no_na[4765:5578])
year_dfs[2013] = (full_df_no_na[5578:6394])
year_dfs[2014] = (full_df_no_na[6394:7210])
year_dfs[2015] = (full_df_no_na[7210:8028])
year_dfs[2016] = (full_df_no_na[8028:])

writer = pd.ExcelWriter('full_features_by_year.xlsx', engine='xlsxwriter')
for i in range(2006, 2017):
    year = str(i)
    year_dfs[i].to_excel(writer, sheet_name=year)
writer.save()
# ------ end creating data frames for each year ------
