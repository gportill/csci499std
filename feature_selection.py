import pandas as pd
import numpy as np
#import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
import sklearn.feature_selection
from sklearn.linear_model import LinearRegression

df = pd.read_excel('./full_features_mig_no_nan_v.xlsx')
x = df.drop('cases_per_person', axis=1)
x = x.drop('cases_raw', axis=1)
x = x.drop('cases', axis=1)
x = x.drop('year', axis=1)
x = x.drop('fips', axis=1)
#x = x.drop('avg_household_size', axis=1)
y = df['cases_per_person']
lm = LinearRegression()

# fit_intercept and normalize => parameters to the linear regression object

lm.fit(x, df.cases_per_person)
print("Estimated intercept coefficient: " + str(lm.intercept_))
print("Number of coefficients: " + str(len(lm.coef_)))
coefs_df = pd.DataFrame(zip(x.columns, lm.coef_), columns=['features', 'estimated coefficients'])
print(coefs_df)

# should year be included as a feature? **
# remove fips and years as a feature

predictions = lm.predict(x)
# plt.scatter(df.rate, predictions)
# plt.xlabel("Actual cases")
# plt.ylabel("Predicted cases")
# plt.title("Actual cases vs. predicted cases")
# plt.show()

print(df.cases_per_person)
print(predictions)

mseFull = np.mean((df.cases_per_person - lm.predict(x))**2)
print(mseFull)

# how to use validation set?

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, df.cases_per_person, test_size=0.2, random_state=5)

lm = LinearRegression()

num_folds = 3
cv_models = model_selection.cross_validate(LinearRegression(), x, y, cv=num_folds, return_estimator=True)
cross_val_predict_data = model_selection.cross_val_predict(LinearRegression(), x, y, cv=num_folds)

plt.figure(figsize=(10,8))
plt.scatter(y, cross_val_predict_data)
plt.xlim(-0.010, 0.020)
plt.ylim(-0.010, 0.020)
plt.ylabel("prediction", fontsize=22)
plt.xlabel("true Y", fontsize=22)
plt.title("Linear Regression")

feature_coefficients_arr = np.array([m.coef_ for m in cv_models["estimator"]])
feature_coefficients_df = pd.DataFrame(feature_coefficients_arr, columns=list(x))
feature_coefficients_df = feature_coefficients_df.agg(["min","median","max"], axis=0).transpose()
feature_coefficients_df = feature_coefficients_df.reindex(feature_coefficients_df.median(axis=1).abs().sort_values().index)

top_20_features = feature_coefficients_df.tail(20)
print(top_20_features)

rfecv = sklearn.feature_selection.RFECV(estimator=LinearRegression(), step=1, cv=5,
              scoring='neg_mean_squared_error', n_jobs=-1)
rfecv.fit(x,y)

fig, ax = plt.subplots(1,1,figsize=(10,8))
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.xlabel("Number of features selected",fontsize=22)
plt.ylabel("Cross validation score (negative mean square error)",fontsize=22)


from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(max_depth=4, random_state=0,n_estimators=100)
regr.fit(x, y)


plt.show()
