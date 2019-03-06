import pandas as pd    # pandas (for reading and handling data in dataframes)

import numpy as np     # matrix/linear algebra library

#from scipy import stats# prob/stats library to get distribution information

#import os              # platform independent filesystem manipulations

#from collections import Counter

#from sklearn import model_selection, kernel_ridge, linear_model, metrics, feature_selection, preprocessing

# plotting libraries
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-paper')

CSV_DATA = "../ChlamydiaData.csv"

fips_codes = "../fips_codes.txt"

fips = []
counties = []

with open(fips_codes, "r") as filestream:
    for line in filestream:
        currentLine = line.split(",")
        fips.append(str(currentLine[1]) + str(currentLine[2]))
        counties.append((str(currentLine[3]) + ", " + str(currentLine[0])).lower())

fips_dict = dict(zip(counties, fips))



raw_df = pd.read_csv(CSV_DATA)

#print(raw_df)
for index, val in enumerate(raw_df["Geography"]):
    if val.lower() in fips_dict:
        raw_df["Geography"][index] = fips_dict[val.lower()]
    else:
        print(raw_df["Geography"][index])



print(raw_df)