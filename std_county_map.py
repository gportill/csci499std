import pandas as pd    # pandas (for reading and handling data in dataframes)

import numpy as np     # matrix/linear algebra library

#from scipy import stats# prob/stats library to get distribution information

#import os              # platform independent filesystem manipulations

#from collections import Counter

#from sklearn import model_selection, kernel_ridge, linear_model, metrics, feature_selection, preprocessing

# plotting libraries
import matplotlib
import matplotlib.pyplot as plt
import plotly
plotly.tools.set_credentials_file(username='carolinechocholak', api_key='zohBCz0bcwuwzFWvqd3d')
plotly.__version__
import plotly.plotly as py
import plotly.figure_factory as ff

plt.style.use('seaborn-paper')

CSV_DATA = "./ChlamydiaData.csv"

fips_codes = "./fips_codes.txt"

fips = []
counties = []

# reading in fips codes
with open(fips_codes, "r") as filestream:
    for line in filestream:
        currentLine = line.split(",")
        fips.append(str(currentLine[1]) + str(currentLine[2]))
        counties.append((str(currentLine[3]) + ", " + str(currentLine[0])).lower())
# creating dictionary with county names and fips codes
fips_dict = dict(zip(counties, fips))


# reading in data from CDC
raw_df = pd.read_csv(CSV_DATA)

# collecting only data from year 2000
year_2000 = raw_df.loc[raw_df['Year'] == 2000]


to_drop = []

# looping through and changing the county names to fips codes, keeping track of those with
# county names that do not match
for idx, val in year_2000.iterrows():
    if year_2000["Geography"][idx].lower() in fips_dict:
        year_2000["Geography"][idx] = fips_dict[year_2000["Geography"][idx].lower()]
    else:
        print(year_2000["Geography"][idx].lower())
        print(idx)
        to_drop.append(year_2000["Geography"][idx])

# dropping the county names with no fips code
for x in to_drop:
    year_2000 = year_2000[year_2000.Geography != x]

# changing rate to -1 if they do not have data available
for index, val in year_2000.iterrows():
    if year_2000["Rate per 100000"][index] == "Data not available":
        year_2000["Rate per 100000"][index] = "-1"

# creating lists of data for fips and
fips = year_2000['Geography'].tolist()
rate_per_hundred_thousand = year_2000['Rate per 100000'].tolist()
rate_per_hundred_thousand = [float(i) for i in rate_per_hundred_thousand]

print(fips)
print(rate_per_hundred_thousand)

colorscale = ["#171c42","#223f78","#1267b2","#4590c4","#8cb5c9","#b6bed5","#dab2be",
              "#d79d8b","#c46852","#a63329","#701b20","#3c0911"]
endpts = list(np.linspace(-1, 500, len(colorscale) - 1))

fig = ff.create_choropleth(
    fips=fips, values=rate_per_hundred_thousand, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    legend_title='% change', title='% Change in Alcohol User Disorders between 1980-2014'
)
py.plot(fig, filename='Rate per 100,000 of Chlamydia Data in year 2000')

#for x in
#print(raw_df)
# for index, val in enumerate(raw_df["Geography"]):
#     if val.lower() in fips_dict:
#         raw_df["Geography"][index] = fips_dict[val.lower()]
#     #else:
        #print(raw_df["Geography"][index])



#print(raw_df)

# fips_codes = "./fips_codes.txt"
#
# fips = []
# counties = []
#
# # reading in fips codes
# with open(fips_codes, "r") as filestream:
#     for line in filestream:
#         currentLine = line.split(",")
#         fips.append(str(currentLine[1]) + str(currentLine[2]))
#         counties.append((str(currentLine[3]) + ", " + str(currentLine[0])).lower())
# # creating dictionary with county names and fips codes
# fips_dict = dict(zip(counties, fips))
# print(fips_dict)
