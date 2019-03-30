import pandas as pd

census_files = ["./census_data/2006_census_with_total_pop.csv", "./census_data/2007_census_with_total_pop.csv", "./census_data/2008_census_with_total_pop.csv", "./census_data/2009_census_with_total_pop.csv", "./census_data/2010_census_with_total_pop.csv", "./census_data/2011_census_with_total_pop.csv", "./census_data/2012_census_with_total_pop.csv", "./census_data/2013_census_with_total_pop.csv", "./census_data/2014_census_with_total_pop.csv", "./census_data/2015_census_with_total_pop.csv", "./census_data/2016_census_with_total_pop.csv"]

# census_files = ["./census_data/2006_census_with_total_pop.csv"]

census_dfs = {}

year = 2005

for file in census_files:
    year += 1
    # print(str(year))
    key = str(year) + "_census"
    census_dfs[key] = pd.read_csv(file, encoding='latin-1', index_col=False)

print(census_dfs)

# for df in census_dfs:
#     print(census_dfs[df].head())

print(census_dfs["2006_census"].columns.values)
