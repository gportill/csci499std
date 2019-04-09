import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.model_selection
from sklearn.linear_model import LogisticRegression
import sklearn.metrics

df = pd.read_excel('./full_features_no_mig_NO_NAN1.xlsx')
df = df.drop('year', axis=1)
df = df.drop('fips', axis=1)
x = df.drop('rate', axis=1)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, df.rate, test_size=0.2, random_state=5)

lm = LogisticRegression()
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

coefs_df = pd.DataFrame(zip(x.columns, lm.coef_), columns=['features', 'estimated coefficients'])
print(coefs_df)

# ---- Residual graph ----
plt.scatter(lm.predict(x_train), lm.predict(x_train) - y_train, c='b', alpha=0.5)
plt.scatter(lm.predict(x_test), lm.predict(x_test) - y_test, c='g')
plt.hlines(y=0, xmin=0, xmax=60000)
plt.title('Residual plot using training (blue) and test (green) data')
plt.ylabel('Residuals')
plt.show()
# ----------------

# ---- Residual graph of ratio between predicted and actual----
plt.scatter(lm.predict(x_train), (lm.predict(x_train) - y_train) / y_train, c='b', alpha=0.5)
plt.scatter(lm.predict(x_test), (lm.predict(x_test) - y_test) / y_test, c='g')
plt.hlines(y=0, xmin=0, xmax=60000)
plt.title('Residual plot using training (blue) and test (green) data')
plt.ylabel('Residuals')
plt.show()
# ----------------

# ---- Actual vs. y_train ----
plt.scatter(y_train, pred_train)
plt.xlabel("Actual cases")
plt.ylabel("Predicted cases")
plt.title("Actual cases vs. predicted cases in y_train")
plt.show()
# ----------------------------

# ---- Actual vs. y_test ----
plt.scatter(y_test, pred_test)
plt.xlabel("Actual cases")
plt.ylabel("Predicted cases")
plt.title("Actual cases vs. predicted cases in y_test")
plt.show()
# ----------------------------

r2 = sklearn.metrics.r2_score(y_test, pred_test)
print("r2: " + str(r2))
