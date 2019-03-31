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
    print(std_dfs[key].head(5))

# --------- Read in all fips codes and associate them with county names --------
fips_codes = "./fips_codes.txt"
fips = []
counties = []

with open(fips_codes, "r") as filestream:
    for line in filestream:
        currentLine = line.split(",")
        fips.append(str(currentLine[1]) + str(currentLine[2]))
        counties.append((str(currentLine[3]) + ", " + str(currentLine[0])).lower())
# creating dictionary with county names and fips codes
fips_dict = dict(zip(counties, fips))
# --------- End reading in all fips codes and associate them with county names --------

# --------- Replace county names with FIPS codes in Geography column ---------
for i in range(2006, 2017):
    df = std_dfs[str(i)]
    to_drop = []

    # looping through and changing the county names to fips codes, keeping track of those with
    # county names that do not match
    for idx, val in df.iterrows():
        if df["Geography"][idx].lower() in fips_dict:
            df["Geography"][idx] = fips_dict[df["Geography"][idx].lower()]
        else:
            print(df["Geography"][idx].lower())
            print(idx)
            to_drop.append(df["Geography"][idx])

    # dropping the county names with no fips code
    for x in to_drop:
        df = df[df.Geography != x]
# --------- End replacing county names with FIPS codes in Geography column ---------
