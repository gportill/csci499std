import pandas as pd
import read_data

counties_unavailable = ['17003',
                '17005',
                '17007',
                '17009',
                '17011',
                '17013',
                '17015',
                '17017',
                '17021',
                '17023',
                '17025',
                '17027',
                '17029',
                '17033',
                '17035',
                '17039',
                '17041',
                '17045',
                '17047',
                '17049',
                '17051',
                '17053',
                '17055',
                '17057',
                '17059',
                '17061',
                '17063',
                '17065',
                '17067',
                '17069',
                '17071',
                '17073',
                '17075',
                '17077',
                '17079',
                '17081',
                '17083',
                '17085',
                '17087',
                '17095',
                '17101',
                '17103',
                '17105',
                '17107',
                '17109',
                '17117',
                '17121',
                '17123',
                '17125',
                '17127',
                '17129',
                '17131',
                '17133',
                '17135',
                '17137',
                '17139',
                '17141',
                '17145',
                '17147',
                '17149',
                '17151',
                '17153',
                '17155',
                '17157',
                '17159',
                '17165',
                '17169',
                '17171',
                '17173',
                '17175',
                '17177',
                '17181',
                '17185',
                '17187',
                '17189',
                '17191',
                '17193',
                '17195',
                '17199',
                '17203']

def get_county_adjacency():
    rd = read_data.ReadData()
    rd.read_std_data()  # must be done before reading neighbors
    adjacency_dict = rd.read_county_neighbors()
    # look up in dictionary (by string FIPS) name of county you want info for.

def make_df(year):
    if year < 2006 or year > 2011:
        print("year must be [2006, 2011]")
        return

    dfs = {}  # access by integer year number, not string
    num_training_years = 5
    year_to_predict = year+num_training_years
    t0 = year  # first year of data
    j = 0

    # cols_to_keep_t0 = ['fips', 'total_pop', 'pop_density', 'male', 'female',
    #                    'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
    #                    'never_married', 'cases_per_person']

                       # 'poverty_status_under18_living_in_poverty',
                       # 'poverty_status_18_to_64_living_in_poverty',
                       # 'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_per_person']
    # 'cases', 'cases_raw'

    il_fips = ['17001',
                '17003',
                '17005',
                '17007',
                '17009',
                '17011',
                '17013',
                '17015',
                '17017',
                '17019',
                '17021',
                '17023',
                '17025',
                '17027',
                '17029',
                '17031',
                '17033',
                '17035',
                '17037',
                '17039',
                '17041',
                '17043',
                '17045',
                '17047',
                '17049',
                '17051',
                '17053',
                '17055',
                '17057',
                '17059',
                '17061',
                '17063',
                '17065',
                '17067',
                '17069',
                '17071',
                '17073',
                '17075',
                '17077',
                '17079',
                '17081',
                '17083',
                '17085',
                '17087',
                '17089',
                '17091',
                '17093',
                '17095',
                '17097',
                '17099',
                '17101',
                '17103',
                '17105',
                '17107',
                '17109',
                '17111',
                '17113',
                '17115',
                '17117',
                '17119',
                '17121',
                '17123',
                '17125',
                '17127',
                '17129',
                '17131',
                '17133',
                '17135',
                '17137',
                '17139',
                '17141',
                '17143',
                '17145',
                '17147',
                '17149',
                '17151',
                '17153',
                '17155',
                '17157',
                '17159',
                '17161',
                '17163',
                '17165',
                '17167',
                '17169',
                '17171',
                '17173',
                '17175',
                '17177',
                '17179',
                '17181',
                '17183',
                '17185',
                '17187',
                '17189',
                '17191',
                '17193',
                '17195',
                '17197',
                '17199',
                '17201',
                '17203']


    cols_to_keep = ['fips', 'total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                        'poverty_status_18_to_64_living_in_poverty', 'poverty_status_65older_living_in_poverty',
                        'infected_inflow', 'cases_per_person']

    print("t0: " + str(t0))
    print("year_to_predict: " + str(year_to_predict))

    for i in range(year, year+num_training_years+1):
        df = pd.read_excel('./full_features_by_year.xlsx', sheet_name=str(i), dtype=str)
        # df = df.drop("Unnamed: 0", axis=1)

        # match all rows of years after t0 match the county rows for t0
        # discard rows that there is no data for at t0
        df = df[cols_to_keep]

        # set the index of the dataframe to be the fips code
        df = df.set_index("fips")
        print(df.shape)
        df = df.filter(items=il_fips, axis='index')
        print(df.shape)

        # if i > t0:
        #     df = df[df['fips'].isin(dfs[t0]['fips'])]

        # if i == t0:
        #     df = df[cols_to_keep_t0]
        # else:
        #     df = df[cols_to_keep]

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

    # # now remove fips_t0 for dfs[t0]
    # no more fips to remove
    # dfs[t0] = dfs[t0].drop('fips', axis=1)

    # concatenate all dfs but the year to predict
    full_df = dfs[t0].copy()
    for i in range(t0+1, year_to_predict):
        full_df = full_df.join(dfs[i], how="left")

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

    # full_df.to_excel("time_dep_data.xlsx", na_rep="nan", index=False)

    # -------- begin linear regression --------
    full_df = full_df.dropna()  # //// end copy after this line
    full_df = full_df.astype(float)

    full_df = full_df.dropna()

    file = "./illinois_data/illinois_" + str(year) + "_cpp.xlsx"

    full_df.to_excel(file, na_rep="nan", index=False)


for i in range(2006, 2012):
    make_df(i)
