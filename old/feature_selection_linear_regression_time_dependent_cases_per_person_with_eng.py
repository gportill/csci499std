import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.linear_model import LinearRegression
import sklearn.model_selection as model_selection
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

    # cols_to_keep_t0 = ['fips', 'total_pop', 'pop_density', 'male', 'female',
    #                    'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
    #                    'never_married', 'poverty_status_under18_living_in_poverty',
    #                    'poverty_status_18_to_64_living_in_poverty',
    #                    'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_per_person']
    # 'cases', 'cases_raw'

    cols_to_keep = ['fips', 'total_pop', 'pop_density', 'male', 'female',
                       'age_15_to_17', 'age_18_to_24', 'age_25_to_34', 'pop_15_and_older',
                       'never_married', 'poverty_status_under18_living_in_poverty',
                       'poverty_status_18_to_64_living_in_poverty',
                       'poverty_status_65older_living_in_poverty', 'infected_inflow', 'cases_per_person']

    print("t0: " + str(t0))
    print("year_to_predict: " + str(year_to_predict))

    for i in range(year, year+num_training_years+1):
        df = pd.read_excel('./full_features_by_year.xlsx', sheet_name=str(i), dtype=str)
        #df = df.drop("Unnamed: 0", axis=1)

        # match all rows of years after t0 match the county rows for t0
        # discard rows that there is no data for at t0
        df = df[cols_to_keep]

        df = df.set_index("fips")

        # if i > t0:
        #     df = df[df['fips'].isin(dfs[t0]['fips'])]
        #
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

    # now remove fips_t0 for dfs[t0]
    # dfs[t0] = dfs[t0].drop('fips', axis=1)

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

    # full_df.to_excel("time_dep_data.xlsx", na_rep="nan", index=False)

    # -------- begin linear regression --------
    full_df = full_df.dropna()
    full_df = full_df.astype(float)

    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5

    # -------------Cross Validation --------------------------------
    num_folds = 5
    print("PRINTING SCORES")
    scores = model_selection.cross_val_score(LinearRegression(), x, y, cv=5, scoring='r2')
    print(scores)
    r2_total = 0
    for s in scores:
        r2_total += s
    avg_r2 = r2_total / scores.size
    print("average: " + str(avg_r2))
    cv_models = model_selection.cross_validate(LinearRegression(), x, y, cv=num_folds, return_estimator=True)
    cross_val_predict_data = model_selection.cross_val_predict(LinearRegression(), x, y, cv=num_folds)

    plt.figure(figsize=(10,8))
    plt.scatter(y, cross_val_predict_data)
    plt.scatter(y, cross_val_predict_data)
    plt.xlim(-0.01, 0.05)
    plt.ylim(-0.01, 0.05)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Cross Validation for Actual cases per person vs. predicted cases per person in t0=" + str(year))
    plt.show()

    # ----------------------- Creating Array of Top 20 Features -------------------

    feature_coefficients_arr = np.array([m.coef_ for m in cv_models["estimator"]])
    feature_coefficients_df = pd.DataFrame(feature_coefficients_arr, columns=list(x))
    feature_coefficients_df = feature_coefficients_df.agg(["min","median","max"], axis=0).transpose()
    feature_coefficients_df = feature_coefficients_df.reindex(feature_coefficients_df.median(axis=1).abs().sort_values().index)

    top_20_features = feature_coefficients_df.tail(20)

    print(top_20_features)

    # ------------ Feature Selection ------------------------------------------

    rfecv = sklearn.feature_selection.RFECV(estimator=LinearRegression(), step=1, cv=5,
                  scoring='r2', n_jobs=-1)
    rfecv.fit(x,y)
    print(len(rfecv.grid_scores_))
    fig, ax = plt.subplots(1,1,figsize=(10,8))
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.xlabel("Number of features selected",fontsize=12)
    plt.ylabel("Cross validation score (r^2 value)",fontsize=12)
    plt.title("Feature Selection on Linear Regression for Year T0=" + str(year))
    plt.show()

    # ---------- Linear Regression with Only Top Features -----------------------
    num_top_features = 20
    remove_features = feature_coefficients_df.head(75 - num_top_features)
    print(top_20_features)
    print(len(remove_features.index))
    print(x.columns)
    for f in list(remove_features.index):
        x = x.drop([f], axis=1)
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
    plt.xlabel("Actual Cases Per Person")
    plt.ylabel("Predicted Cases Per Person")
    plt.title("Linear Regression with Top Features for Year T0=" + str(year))
    plt.show()







create_model(2011)
#create_model(2007)
#create_model(2008)
#create_model(2009)
#create_model(2010)
#create_model(2011)
