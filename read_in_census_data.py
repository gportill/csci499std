import pandas as pd

census_files = ["./census_data/2006_census_with_total_pop.csv", "./census_data/2007_census_with_total_pop.csv", "./census_data/2008_census_with_total_pop.csv", "./census_data/2009_census_with_total_pop.csv", "./census_data/2010_census_with_total_pop.csv", "./census_data/2011_census_with_total_pop.csv", "./census_data/2012_census_with_total_pop.csv", "./census_data/2013_census_with_total_pop.csv", "./census_data/2014_census_with_total_pop.csv", "./census_data/2015_census_with_total_pop.csv", "./census_data/2016_census_with_total_pop.csv"]

# census_files = ["./census_data/2006_census_with_total_pop.csv"]

census_dfs = {}

year = 2005

for file in census_files:
    year += 1
    # print(str(year))
    key = str(year)
    census_dfs[key] = pd.read_csv(file, encoding='latin-1', index_col=False)

print(census_dfs)

# for df in census_dfs:
#     print(census_dfs[df].head())

print(census_dfs["2006"].columns.values)
print(census_dfs["2008"].columns.values)

# only difference between 2006 and 2008 is that 2008 has these additional:
# 'SE_A20001_001' 'SE_A20001_002' 'SE_A20001_003' 'SE_A20001_004' 'SE_A20001_005']
# health insurance?