# doesn't work terribly for 2008 but most are still negative

# lm = RandomForestRegressor(n_estimators=6, random_state=5)
# 2008: test r^2 = 0.20

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics


def create_model(year):
    filename = "time_dep_t0_" + str(year) + ".xlsx"
    full_df = pd.read_excel(filename, dtype=float)

    x = full_df.drop('target_t5', axis=1)
    y = full_df.target_t5.astype(float)

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2,
                                                                                random_state=5)
    # add regularization to linear model
    # increase weight of l2 norm or l1 norm
    # elastic net or kernel ridge regression, decision trees, gradient with shallow trees (max_depth = small)
    # hamper 0 make them have less complexity.
    # try less features => bagging regressor to subsample features
    # try changing target
    lm = RandomForestRegressor(n_estimators=10, random_state=5)
    lm.fit(x_train, y_train)
    pred_train = lm.predict(x_train)
    print("training r^2:", sklearn.metrics.r2_score(y_train, pred_train))
    pred_test = lm.predict(x_test)

    r2 = sklearn.metrics.r2_score(y_test, pred_test)
    print("r2: " + str(r2))

    plt.scatter(y_test, pred_test)
    plt.xlabel("Actual cases")
    plt.ylabel("Predicted cases")
    plt.title("Actual cases vs. predicted cases in y_test")
    plt.show()


create_model(2008)
