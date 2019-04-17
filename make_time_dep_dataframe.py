import pandas as pd

# makes a data frame for time dependent modes for CASES-PER-PERSON and WITH ENGINEERED FEATURES
# file name: "time_dep_t0_" + str(year) + ".xlsx"
# full_df = pd.read_excel(filename, dtype=float)

def build_df(year):
    if year < 2006 or year > 2011:
        print("year must be [2006, 2011]")
        return

    dfs = {}  # access by integer year number, not string
    num_training_years = 5
    year_to_predict = year+num_training_years
    t0 = year  # first year of data
    j = 0

    cols_to_keep_t0 = ['fips', 'total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                       'poverty_status_18_to_64_living_in_poverty',
                       'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_per_person']
    # 'cases' => cases_normalized, 'cases_raw'
    # you can select other census variables here, too

    cols_to_keep = ['total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                       'poverty_status_18_to_64_living_in_poverty',
                       'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_per_person']

    print("t0: " + str(t0))
    print("year_to_predict: " + str(year_to_predict))

    for i in range(year, year+num_training_years+1):
        df = pd.read_excel('./full_features_by_year.xlsx', sheet_name=str(i), dtype=str)
        df = df.drop("Unnamed: 0", axis=1)

        # match all rows of years after t0 match the county rows for t0
        # discard rows that there is no data for at t0
        if i > t0:
            df = df[df['fips'].isin(dfs[t0]['fips'])]

        if i == t0:
            df = df[cols_to_keep_t0]
        else:
            df = df[cols_to_keep]

        # update column names for all dfs
        updated_col_names = []
        column_names = df.columns.values
        for name in column_names:
            if i == t0 and name == 'year':
                updated_col_names.append('year')
                continue
            if i == t0 and name == 'fips':
                updated_col_names.append('fips')
                continue
            updated_col_names.append(name + "_t" + str(j))
        df.columns = updated_col_names
        j += 1
        dfs[i] = df

    # now remove fips_t0 for dfs[t0]
    dfs[t0] = dfs[t0].drop('fips', axis=1)

    # concatenate all dfs but the year to predict
    full_df = dfs[t0].copy()
    for i in range(t0+1, year_to_predict):
        full_df = full_df.join(dfs[i])

    # -------- add engineered features -------

    full_df['cases_per_person_t0'] = full_df['cases_per_person_t0'].astype(float)
    full_df['cases_per_person_t1'] = full_df['cases_per_person_t1'].astype(float)
    full_df['cases_per_person_t2'] = full_df['cases_per_person_t2'].astype(float)
    full_df['cases_per_person_t3'] = full_df['cases_per_person_t3'].astype(float)
    full_df['cases_per_person_t4'] = full_df['cases_per_person_t4'].astype(float)

    # diff_cases_t0_t4
    full_df['diff_cases_t0_t4'] = full_df['cases_per_person_t4'] - full_df['cases_per_person_t0']
    # diff_cases_t0_t1
    full_df['diff_cases_t0_t1'] = full_df['cases_per_person_t1'] - full_df['cases_per_person_t0']
    # diff_cases_t1_t2
    full_df['diff_cases_t1_t2'] = full_df['cases_per_person_t2'] - full_df['cases_per_person_t1']
    # diff_cases_t2_t3
    full_df['diff_cases_t2_t3'] = full_df['cases_per_person_t3'] - full_df['cases_per_person_t2']
    # diff_cases_t3_t4
    full_df['diff_cases_t3_t4'] = full_df['cases_per_person_t4'] - full_df['cases_per_person_t3']
    # print(full_df.head())
    # -------- end engineered features --------

    full_df['target_t5'] = dfs[year_to_predict].cases_per_person_t5  # put the variable you want to predict here
    # now that variable (for y) is called target_t5 in the full_df

    full_df = full_df.dropna()

    file = "time_dep_t0_" + str(year) + ".xlsx"

    full_df.to_excel(file, na_rep="nan", index=False)


for i in range(2006, 2012):
    build_df(i)
