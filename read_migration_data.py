import pandas as pd

county_adj_file = "./county_adjacency.txt"

county_adj_df = pd.read_csv(county_adj_file, encoding = "ISO-8859-1", sep='\t', header=None, dtype=str)

print(county_adj_df.head(5))

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
curr_county = (county_adj_df.iloc[0, name_col])

for i in range(1, len(county_adj_df)):
    if not pd.isnull(county_adj_df.iloc[i, name_col]) and i > 1:  # new_county
        # add current list to old_county in dictionary
        name_adj_dict[curr_county] = neighbors
        neighbors = []
        curr_county = county_adj_df.iloc[i, name_col]
    else:
        neighbors.append(county_adj_df.iloc[i, neighbor_name_col])

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