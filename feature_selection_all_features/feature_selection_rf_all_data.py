import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def create_model(year):
    if year < 2006 or year > 2011:
        print("year must be [2006, 2011]")
        return

    file = './all_features_dfs/' + str(year) + 'all_features_cpp.xlsx'
    full_df = pd.read_excel(file, dtype=str)
    full_df = full_df.astype(float)

    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5

    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5

    # ------------------------ Cross Validation ---------------------

    num_folds = 5
    print("PRINTING SCORES")
    scores = sklearn.model_selection.cross_val_score(RandomForestRegressor(n_estimators=100, random_state=5), x, y, cv=5, scoring='r2')
    print(scores)
    r2_total = 0
    for s in scores:
        r2_total += s
    avg_r2 = r2_total / scores.size
    print("average: " + str(avg_r2))
    cv_models = sklearn.model_selection.cross_validate(RandomForestRegressor(n_estimators=100, random_state=5), x, y, cv=num_folds, return_estimator=True)
    cross_val_predict_data = sklearn.model_selection.cross_val_predict(RandomForestRegressor(n_estimators=100, random_state=5), x, y, cv=num_folds)

    plt.figure(figsize=(10,8))
    plt.scatter(y, cross_val_predict_data)
    plt.scatter(y, cross_val_predict_data)
    plt.xlim(-0.01, 0.05)
    plt.ylim(-0.01, 0.05)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Cross Validation for Actual cases per person vs. predicted cases per person in t0=" + str(year))
    plt.show()

    # -------------- Create Array of top 20 features --------------------
    feature_coefficients_arr = np.array([m.feature_importances_ for m in cv_models["estimator"]])
    feature_coefficients_df = pd.DataFrame(feature_coefficients_arr, columns=list(x))
    feature_coefficients_df = feature_coefficients_df.agg(["min","median","max"], axis=0).transpose()
    feature_coefficients_df = feature_coefficients_df.reindex(feature_coefficients_df.median(axis=1).abs().sort_values().index)

    top_20_features = feature_coefficients_df.tail(20)

    print(top_20_features)


    # ------------- Feature Selection -----------------------------------
    rfecv = sklearn.feature_selection.RFECV(estimator=RandomForestRegressor(n_estimators=100, random_state=5), step=1, cv=5,
                                            scoring='r2', n_jobs=-1)
    rfecv.fit(x, y)
    print(len(rfecv.grid_scores_))
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.xlabel("Number of features selected", fontsize=12)
    plt.ylabel("Cross validation score (r^2 value)", fontsize=12)
    plt.title("Feature Selection on Linear Regression for Year T0=" + str(year))
    plt.show()

    # ----------- Random Forests with Only Top Features ----------------

    num_top_features = 10
    remove_features = feature_coefficients_df.head(75 - num_top_features)
    print(top_20_features)
    print(len(remove_features.index))
    print(x.columns)
    for f in list(remove_features.index):
        x = x.drop([f], axis=1)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2,
                                                                                random_state=5)
    lm = RandomForestRegressor(n_estimators=100, random_state=5)
    lm.fit(x_train, y_train)
    pred_train = lm.predict(x_train)
    pred_test = lm.predict(x_test)

    # coefs_df = pd.DataFrame(zip(x.columns, lm.coef_), columns=['features', 'estimated coefficients'])
    # print(coefs_df)

    r2 = sklearn.metrics.r2_score(y_test, pred_test)
    print("r2: " + str(r2))

    plt.scatter(y_test, pred_test)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Actual cases vs. predicted cases in y_test")
    plt.show()


for year in range(2006, 2012):
    create_model(year)
