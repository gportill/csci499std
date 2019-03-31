import pandas as pd

county_adj_file = "./county_adjacency.txt"

county_adj_df = pd.read_csv(county_adj_file, encoding = "ISO-8859-1", sep='\t', header=None, dtype=str)

# store fips as a STRING!
# dictionary of county_name (which is column 0, which column 0 != NaN) to list of neighbor_names
# keep a fips array of county_name to FIPS (string)

name_adj_dict = {}
fips_adj_dict = {}
neighbors = []
name_col = 0
fips_col = 1
neighbor_name_col = 2
neighbor_fips_col = 3
curr_county = county_adj_df.iloc[0, name_col].lower()

for i in range(1, len(county_adj_df)):
    if not pd.isnull(county_adj_df.iloc[i, name_col]) and i > 1:  # new_county
        # add current list to old_county in dictionary
        name_adj_dict[curr_county] = neighbors
        neighbors = []
        curr_county = county_adj_df.iloc[i, name_col].lower()
    else:
        neighbors.append(county_adj_df.iloc[i, neighbor_name_col].lower())

print(name_adj_dict)

#### make fips adj dictionary ####

curr_county = str(county_adj_df.iloc[0, fips_col])
neighbors = []

for i in range(1, len(county_adj_df)):
    if not pd.isnull(county_adj_df.iloc[i, fips_col]) and i > 1:  # new_county
        # add current list to old_county in dictionary
        fips_adj_dict[curr_county] = neighbors
        neighbors = []
        curr_county = str(county_adj_df.iloc[i, fips_col])
    else:
        neighbors.append(str(county_adj_df.iloc[i, neighbor_fips_col]))

print(fips_adj_dict)

# if the "county name" index 5 contains "total migration" or "other" or "tot mig" then exclude that row

# list of state abbreviations
state_abbrev = ["AR", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "IA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "MD", "ME",
        "MI", "MN", "MO", "MS", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

year_codes = ["0506", "0607", "0708", "0809", "0910", "1011", "1112", "1213", "1314", "1415", "1516"]

migration_dfs = {}

# for i in range(0,7): # 0506 to 1011
#     for state in state_abbrev:
#         file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state + "i.xls"
#         # read csv for this file
#         # drop rows (as on stack overflow) for the specific words
#         # then assemble the fips from first four columns
#         # create data frame with the 2 fips and the numbers from pandas
#         raw_df = pd.read_excel(file, encoding = "ISO-8859-1")
#         print(raw_df)


i = 0
state = "AK"
file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state + "i.xls"
# read csv for this file
# drop rows (as on stack overflow) for the specific words
# then assemble the fips from first four columns
# create data frame with the 2 fips and the numbers from pandas
col_names = ["state_fips1", "county_fips1", "state_fips2", "county_fips2", "state", "description", "num_returns",
             "num_exemptions", "agg_adj_gross_income"]

raw_df = pd.read_excel(file, encoding = "ISO-8859-1", skiprows=8, header=None, names=col_names, dtype=str)
print(len(raw_df.index))
raw_df = raw_df[~raw_df.description.str.contains("Total")]
raw_df = raw_df[~raw_df.description.str.contains("Other")]
raw_df = raw_df[~raw_df.description.str.contains("Tot")]
raw_df = raw_df[~raw_df.description.str.contains("Foreign")]
raw_df = raw_df[~raw_df.description.str.contains("Non-Migrants")]
raw_df = raw_df[~raw_df.description.str.contains("Non-Migrant")]
print(len(raw_df.index))
print(raw_df.head(5))

destination_fips = []
origin_fips = []
num_exemptions = []

for i in range(0,len(raw_df)):
    # print(raw_df.iloc[i]['state_fips1'])
    dest_fips = str(raw_df.iloc[i]['state_fips1']) + str(raw_df.iloc[i]['county_fips1'])
    ori_fips = str(raw_df.iloc[i]['state_fips2']) + str(raw_df.iloc[i]['county_fips2'])
    num_exemps = raw_df.iloc[i]['num_exemptions']
    # print(dest_fips + " " + ori_fips + " " + num_exemps)
    destination_fips.append(dest_fips)
    origin_fips.append(ori_fips)
    num_exemptions.append(num_exemps)

d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}

df = pd.DataFrame(d)

print(df.head(5))
