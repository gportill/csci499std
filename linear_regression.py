import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.linear_model import LinearRegression

df = pd.read_excel('./full_features_no_mig_NO_NAN1.xlsx')
x = df.drop('rate', axis=1)
lm = LinearRegression()

# fit_intercept and normalize => parameters to the linear regression object

lm.fit(x, df.rate)
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

print(df.rate)
print(predictions)

mseFull = np.mean((df.rate - lm.predict(x))**2)
print(mseFull)

# how to use validation set?

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, df.rate, test_size=0.2, random_state=5)

lm = LinearRegression()
lm.fit(x_train, y_train)
pred_train = lm.predict(x_train)
print("pred_train: " + str(list(pred_train)))
pred_test = lm.predict(x_test)
print("pred_test: " + str(list(pred_test)))
print("y_test: " + str(list(y_test)))

mseTrain = np.mean((y_train - lm.predict(x_train))**2)
mseTest = np.mean((y_test - lm.predict(x_test))**2)
print("mseTrain: " + str(mseTrain))
print("mseTest: " + str(mseTest))

plt.scatter(lm.predict(x_train), lm.predict(x_train) - y_train, c='b', s=40, alpha=0.5)
plt.scatter(lm.predict(x_test), lm.predict(x_test) - y_test, c='g', s=40)
plt.hlines(y=0, xmin=0, xmax=30000)
plt.title('Residual plot using training (blue) and test (green) data')
plt.ylabel('Residuals')
plt.show()
