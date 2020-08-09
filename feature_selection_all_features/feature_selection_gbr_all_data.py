import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.model_selection
import sklearn.feature_selection
from sklearn.ensemble import GradientBoostingRegressor
import sklearn.metrics

# Builds a GBR to predict the number of cases per person in the 6th year,
# using 5 years of past data as features.
# Ex: if year parameter is 2006, the years 2006-2010 are used to build model
#     and the number of cases per person in 2011 is predicted.

# The code performs 5-fold cross validation, calculates average r^2 and MSE,
# creates and saves a plot of cross validation results (actual cases s. predicted cases),
# finds the top 20 most important features, performs feature selection,
# and creates a GBR with the selected features.

# Plots are saved in all_features_dfs directory.

def create_model(year):
    if year < 2006 or year > 2011:
        print("year must be [2006, 2011]")
        return

    print("------ YEAR " + str(year) + " ------")

    # load data
    file = '../all_features_dfs/' + str(year) + 'all_features_cpp.xlsx'
    full_df = pd.read_excel(file, dtype=str)
    full_df = full_df.astype(float)
    full_df = full_df.drop('fips', axis=1)

    # we will predict cases_per_person in 6th year [target_t5]
    # drop this variable from data frame so that it is not used in predictions
    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5

    # ------ cross validation ------
    num_folds = 5
    scores = {'r2': 'r2',
              'mse': 'neg_mean_squared_error'}

    scores = sklearn.model_selection.cross_validate(GradientBoostingRegressor(max_depth=2), x, y, cv=5, scoring=scores)
    print("test_r2 array:", scores['test_r2'])
    print("test_mse array:", scores['test_mse'])

    # ------ calculate average r2 ------
    r2_total = 0
    for s in scores['test_r2']:
        r2_total += s
    avg_r2 = r2_total / 5
    print("CV average r2:", str(avg_r2))
    # ----- end calculate average r2 -----

    # ----- calculate average mse -----
    mse_total = 0
    for s in scores['test_mse']:
        mse_total += s
    avg_mse = mse_total / 5
    print("CV average mse:", avg_mse)
    # ----- end calculate average mse -----

    cv_models = sklearn.model_selection.cross_validate(GradientBoostingRegressor(max_depth=2), x, y, cv=num_folds, return_estimator=True)
    cross_val_predict_data = sklearn.model_selection.cross_val_predict(GradientBoostingRegressor(max_depth=2), x, y, cv=num_folds)

    # plot the cross validation results (actual number of cases per person vs. predicted cases per person)
    plt.figure(figsize=(10,8))
    plt.scatter(y, cross_val_predict_data)
    plt.scatter(y, cross_val_predict_data)
    plt.xlim(-0.01, 0.05)
    plt.ylim(-0.01, 0.05)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Cross Validation for Actual cases per person vs. predicted cases per person in t0=" + str(year))
    plt.savefig("../all_feature_figures/gbr/gbr_" + str(year) + "_cv_no_feature_selection.png")
    plt.clf()

    # ------ create array of 20 top features ------
    feature_coefficients_arr = np.array([m.feature_importances_ for m in cv_models["estimator"]])
    feature_coefficients_df = pd.DataFrame(feature_coefficients_arr, columns=list(x))
    feature_coefficients_df = feature_coefficients_df.agg(["min","median","max"], axis=0).transpose()
    feature_coefficients_df = feature_coefficients_df.reindex(feature_coefficients_df.median(axis=1).abs().sort_values().index)

    top_20_features = feature_coefficients_df.tail(20)  # pull the 20 most important features

    print()
    print("Top 20 features")
    print(top_20_features)  # output the top features

    # ------ feature selection ------
    rfecv = sklearn.feature_selection.RFECV(estimator=GradientBoostingRegressor(max_depth=2), step=1, cv=5,
                  scoring='r2', n_jobs=-1)
    rfecv.fit(x, y)
    fig, ax = plt.subplots(1,1,figsize=(10,8))

    # create a plot with the features of feature selection
    # the plot examines performance of the GBR based on r^2 depending on the number of features selected
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.xlabel("Number of features selected",fontsize=12)
    plt.ylabel("Cross validation score (r^2 value)",fontsize=12)
    plt.title("Feature Selection on GBR for Year T0=" + str(year))
    # plt.show()
    plt.savefig("../all_feature_figures/gbr/gbr_" + str(year) + "_feature_selection_plot.png")
    plt.clf()

    # ------------- Gradient Boosted Regression with only top features ----------------------
    num_top_features = 20
    remove_features = feature_coefficients_df.head(75 - num_top_features)
    for f in list(remove_features.index):
        x = x.drop([f], axis=1)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2, random_state=5)

    # create GBR with only top features
    lm = GradientBoostingRegressor(max_depth=2)
    lm.fit(x_train, y_train)
    pred_train = lm.predict(x_train)
    pred_test = lm.predict(x_test)

    # Determine r^2 for GBR on top 20 features
    r2 = sklearn.metrics.r2_score(y_test, pred_test)
    print("r2 for top 20 features (no CV): " + str(r2))

    # Plot the performance of GBR using top 20 features
    # Plot compares actual cases per person and predicted cases per person for each county
    plt.scatter(y_test, pred_test)
    plt.xlabel("Actual Cases Per Person")
    plt.ylabel("Predicted Cases Per Person")
    plt.title("Gradient Boosted Regression with Top Features for Year T0=" + str(year))
    plt.savefig("../all_feature_figures/gbr/gbr_" + str(year) + "_no_cv_only_top_features.png")
    plt.clf()

    print()


for i in range(2006, 2012):
    create_model(i)
