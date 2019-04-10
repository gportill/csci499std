import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.linear_model import LinearRegression
import sklearn.metrics


def create_model(year):
    if year < 2006 or year > 2011:
        print("year must be [2006, 2011]")
        return

    dfs = {}  # access by integer year number, not string
    num_training_years = 5
    year_to_predict = year+num_training_years
    t0 = year  # first year of data
    j = 0

    print("t0: " + str(t0))
    print("year_to_predict: " + str(year_to_predict))

    for i in range(year, year+num_training_years+1):
        df = pd.read_excel('./full_features_by_year.xlsx', sheet_name=str(i), dtype=str)
        df = df.drop("Unnamed: 0", axis=1)

        # match all rows of years after t0 match the county rows for t0
        # discard rows that there is no data for at t0
        if i > t0:
            df = df[df['fips'].isin(dfs[t0]['fips'])]

        # remove year and fips columns for ALL data frames
        if not i == t0:
            df = df.drop('fips', axis=1) # except don't remove fips_t0 for now because we need it
        df = df.drop('year', axis=1)
        df = df.drop(['cases_raw', 'cases_per_person'], axis=1)  # TODO remove any variables you want to here

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

    print(full_df.head())


create_model(2006)
