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

    cols_to_keep_t0 = ['fips', 'total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                       'poverty_status_18_to_64_living_in_poverty',
                       'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_raw']
    # 'cases', 'cases_per_person'

    cols_to_keep = ['total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                       'poverty_status_18_to_64_living_in_poverty',
                       'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_raw']

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

    full_df['target_t5'] = dfs[year_to_predict].cases_raw_t5  # put the variable you want to predict here
    # now that variable (for y) is called target_t5 in the full_df

    # full_df.to_excel("time_dep_data.xlsx", na_rep="nan", index=False)

    # -------- begin linear regression --------
    full_df = full_df.dropna()

    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2,
                                                                                random_state=5)
    lm = LinearRegression()
    lm.fit(x_train, y_train)
    pred_train = lm.predict(x_train)
    pred_test = lm.predict(x_test)

    coefs_df = pd.DataFrame(zip(x.columns, lm.coef_), columns=['features', 'estimated coefficients'])
    print(coefs_df)

    r2 = sklearn.metrics.r2_score(y_test, pred_test)
    print("r2: " + str(r2))

    plt.scatter(y_test, pred_test)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Actual cases vs. predicted cases in y_test")
    plt.show()


# create_model(2006)
# create_model(2007)
# create_model(2008)
create_model(2009)
# create_model(2010)
# create_model(2011)
