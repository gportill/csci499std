import pandas as pd

county_adj_file = "./county_adjacency.txt"

county_adj_df = pd.read_csv(county_adj_file, encoding="ISO-8859-1", sep='\t', header=None, dtype=str)

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
# state_abbrev = ["AL", "AK", "AZ", "AR"]

state_abbrev = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME",
                "MI", "MN", "MO", "MS", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

year_codes = ["0506", "0607", "0708", "0809", "0910", "1011", "1112", "1213", "1314", "1415", "1516"]

migration_dfs = {}
# ---------

year = 2006
for i in range(0, 6):  # 0506 to 1011
    # print("iiiiiii: " + str(i))
    # print(year_codes[i])
    # print("YEAR::::::::" + str(year))
    destination_fips = []
    origin_fips = []
    num_exemptions = []

    for state in state_abbrev:
        # print("state: " + state)
        # file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state + "i.xls"

        if i == 0:
            file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state + "i.xls"
        elif i == 1:
            state_name = state.lower()
            state_name = state_name.capitalize()
            file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state_name + "i.xls"
        elif i == 2 or i == 3:
            state_name = state.lower()
            state_name = state_name.capitalize()
            file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + "i" + state + ".xls"
        elif i == 4:
            file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + "i" + state + ".xls"
        elif i == 5:
            state_name = state.lower()
            file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + "i" + state_name + ".xls"

        raw_df = pd.read_excel(file, encoding="ISO-8859-1")
        col_names = ["state_fips1", "county_fips1", "state_fips2", "county_fips2", "state", "description",
                     "num_returns",
                     "num_exemptions", "agg_adj_gross_income"]

        raw_df = pd.read_excel(file, encoding="ISO-8859-1", skiprows=8, header=None, names=col_names, dtype=str)
        # print(len(raw_df.index))
        raw_df = raw_df[~raw_df.description.str.contains("Total", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Other", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Tot", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Foreign", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrants", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrant", na=False)]
        # print(len(raw_df.index))
        # print(raw_df.head(5))

        for j in range(0, len(raw_df)):
            # print(raw_df.iloc[i]['state_fips1'])
            dest_fips = str(raw_df.iloc[j]['state_fips1']) + str(raw_df.iloc[j]['county_fips1'])
            ori_fips = str(raw_df.iloc[j]['state_fips2']) + str(raw_df.iloc[j]['county_fips2'])
            num_exemps = raw_df.iloc[j]['num_exemptions']
            # print(dest_fips + " " + ori_fips + " " + num_exemps)
            destination_fips.append(dest_fips)
            origin_fips.append(ori_fips)
            num_exemptions.append(num_exemps)

    print(destination_fips)
    print(origin_fips)
    print(num_exemptions)

    d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
    df = pd.DataFrame(d)
    # print(df.head(5))
    migration_dfs[str(year)] = df
    print("year: " + str(year))
    print(migration_dfs[str(year)].head(5))
    print()
    year += 1

for i in range(0,5): # 1112 to 1516
    # xls = pd.ExcelFile('path_to_file.xls')
    destination_fips = []
    origin_fips = []
    num_exemptions = []

    for state in state_abbrev:
        # print("state: " + state)
        state_name = state.lower()
        file = "./migration_data/" + year_codes[i] + "migrationdata/" + year_codes[i] + state_name + ".xls"

        full_data = pd.ExcelFile(file)

        raw_df = pd.read_excel(full_data, 'County Inflow', encoding="ISO-8859-1")
        col_names = ["state_fips1", "county_fips1", "state_fips2", "county_fips2", "state", "description",
                     "num_returns",
                     "num_exemptions", "agg_adj_gross_income"]

        raw_df = pd.read_excel(file, encoding="ISO-8859-1", skiprows=8, header=None, names=col_names, dtype=str)
        # print(len(raw_df.index))
        raw_df = raw_df[~raw_df.description.str.contains("Total", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Other", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Tot", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Foreign", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrants", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrant", na=False)]
        # print(len(raw_df.index))
        # print(raw_df.head(5))

        for j in range(0, len(raw_df)):
            # print(raw_df.iloc[i]['state_fips1'])
            dest_fips = str(raw_df.iloc[j]['state_fips1']) + str(raw_df.iloc[j]['county_fips1'])
            ori_fips = str(raw_df.iloc[j]['state_fips2']) + str(raw_df.iloc[j]['county_fips2'])
            num_exemps = raw_df.iloc[j]['num_exemptions']
            # print(dest_fips + " " + ori_fips + " " + num_exemps)
            destination_fips.append(dest_fips)
            origin_fips.append(ori_fips)
            num_exemptions.append(num_exemps)

    print(destination_fips)
    print(origin_fips)
    print(num_exemptions)

    d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
    df = pd.DataFrame(d)
    # print(df.head(5))
    migration_dfs[str(year)] = df
    print("year: " + str(year))
    print(migration_dfs[str(year)].head(5))
    print()
    year += 1
