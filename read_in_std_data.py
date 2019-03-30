import pandas as pd

std_files = ["./chlam_data/2006_chlamydia.csv", "./chlam_data/2007_chlamydia.csv", "./chlam_data/2008_chlamydia.csv",
             "./chlam_data/2009_chlamydia.csv", "./chlam_data/2010_chlamydia.csv", "./chlam_data/2011_chlamydia.csv",
             "./chlam_data/2012_chlamydia.csv", "./chlam_data/2013_chlamydia.csv", "./chlam_data/2014_chlamydia.csv",
             "./chlam_data/2015_chlamydia.csv", "./chlam_data/2016_chlamydia.csv"]

std_dfs = {}

year = 2005

for file in std_files:
    year += 1
    key = str(year)
    std_dfs[key] = pd.read_csv(file, encoding='latin-1')
