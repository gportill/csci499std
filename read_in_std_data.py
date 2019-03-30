import pandas as pd

std_files = ["./all_std_data/2006_std.csv", "./all_std_data/2007_std.csv", "./all_std_data/2008_std.csv", "./all_std_data/2009_std.csv", "./all_std_data/2010_std.csv", "./all_std_data/2011_std.csv", "./all_std_data/2012_std.csv", "./all_std_data/2013_std.csv", "./all_std_data/2014_std.csv", "./all_std_data/2015_std.csv", "./all_std_data/2016_std.csv"]

std_dfs = {}

year = 2005

for file in std_files:
    year += 1
    print(str(year))
    key = str(year)
    std_dfs[key] = pd.read_csv(file, encoding='latin-1')
    # should index_col be true or false?

print(std_dfs)

# for df in census_dfs:
#     print(census_dfs[df].head())

# print(census_dfs["2006"].columns.values)
# print(census_dfs["2008"].columns.values)

# only difference between 2006 and 2008 is that 2008 has these additional:
# 'SE_A20001_001' 'SE_A20001_002' 'SE_A20001_003' 'SE_A20001_004' 'SE_A20001_005']
# health insurance?