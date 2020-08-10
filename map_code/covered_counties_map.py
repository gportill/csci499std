import pandas as pd    # pandas (for reading and handling data in dataframes)

import numpy as np     # matrix/linear algebra library

# plotting libraries
import matplotlib
import matplotlib.pyplot as plt
import plotly
plotly.tools.set_credentials_file(username='carolinechocholak', api_key='zohBCz0bcwuwzFWvqd3d')
# plotly.__version__
import plotly.plotly as py
import plotly.figure_factory as ff

plt.style.use('seaborn-paper')

# CSV_DATA = "./ChlamydiaData.csv"

fips_codes = "./data/fips_and_county_info/fips_codes.txt"

included_fips_csv = "../data/fips_and_county_info/included_fips.csv"
included_fips_list = []
with open(included_fips_csv, "r") as filestream:
    for line in filestream:
        line = line[:5]
        included_fips_list.append(line)
print(included_fips_list)

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
fips_dict_values = list(fips_dict.values())
print(fips_dict_values)

vals_to_map = {}
for fipscode in fips_dict_values:
    if fipscode in included_fips_list:
        vals_to_map[fipscode] = 100
    else:
        vals_to_map[fipscode] = 0
print(vals_to_map)

colorscale = ["#171c42","#223f78","#1267b2","#4590c4","#8cb5c9","#b6bed5","#dab2be",
              "#d79d8b","#c46852","#a63329","#701b20","#3c0911"]
endpts = list(np.linspace(0, 100, len(colorscale) - 1)) # maybe try to as third argument

fig = ff.create_choropleth(
    fips=list(vals_to_map.keys()), values=list(vals_to_map.values()), colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    legend_title='Coverage', title='Covered/Not Covered'
)
py.plot(fig, filename='Covered Counties')
