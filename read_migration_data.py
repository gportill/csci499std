import pandas as pd
from pathlib import Path

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

# print(name_adj_dict)

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

# print(fips_adj_dict)

# if the "county name" index 5 contains "total migration" or "other" or "tot mig" then exclude that row

# list of state abbreviations
# state_abbrev = ["AL", "AK", "AZ", "AR"]

state_abbrev = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME",
                "MI", "MN", "MO", "MS", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

year_codes = ["0506", "0607", "0708", "0809", "0910", "1011"]

migration_dfs = {}
# ---------

year = 2006
for i in range(0, 6):  # 0506 to 1011
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
        raw_df = raw_df[~raw_df.description.str.contains("Non-migrants", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-migrant", na=False)]
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

    d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
    df = pd.DataFrame(d)
    # print(df.head(5))
    migration_dfs[str(year)] = df
    print("year: " + str(year))
    print(migration_dfs[str(year)].head(5))
    print()
    year += 1


########## now read 2011-2012 files ##########

year_codes = ["1112", "1213", "1314", "1415", "1516"]
year = 2012

for i in range(0,5): # 1112 to 1516
    # xls = pd.ExcelFile('path_to_file.xls')
    destination_fips = []
    origin_fips = []
    num_exemptions = []

    for state in state_abbrev:
        # print("state: " + state)
        state_name = state.lower()
        file = "./migration_data/" + year_codes[i] + "migrationdata/" + year_codes[i] + state_name + ".xls"
        config = Path(file)
        if not config.is_file():
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            print("_________________ NO FILE WITH NAME : " + file + " ________________")
            continue



        # full_data = pd.ExcelFile(file)

        col_names = ["state_fips1", "county_fips1", "state_fips2", "county_fips2", "state", "description",
                     "num_returns",
                     "num_exemptions", "agg_adj_gross_income"]
        raw_df = pd.read_excel(file, 'County Inflow', encoding="ISO-8859-1", skiprows=6, header=None,
                               names=col_names, dtype=str)

        # raw_df = pd.read_excel(file, encoding="ISO-8859-1", skiprows=6, header=None, names=col_names, dtype=str)
        # print(len(raw_df.index))
        raw_df = raw_df[~raw_df.description.str.contains("Total", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Other", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Tot", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Foreign", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrants", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-migrants", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-Migrant", na=False)]
        raw_df = raw_df[~raw_df.description.str.contains("Non-migrant", na=False)]
        raw_df = raw_df[~raw_df.state_fips1.str.contains("suppressed", na=False)]
        raw_df = raw_df[~raw_df.state_fips1.str.contains("aggregates", na=False)]
        raw_df = raw_df[~raw_df.state_fips1.str.contains("Source", na=False)]
        # print(len(raw_df.index))
        # print(raw_df.head(5))

        for j in range(0, len(raw_df)):
            # print(raw_df.iloc[i]['state_fips1'])
            sf1 = raw_df.iloc[j]['state_fips1']
            cf1 = raw_df.iloc[j]['county_fips1']
            sf2 = raw_df.iloc[j]['state_fips2']
            cf2 = raw_df.iloc[j]['county_fips2']

            if len(sf1) < 2:
                sf1 = "0" + sf1
            if float(cf1) < 10:
                cf1 = "00" + str(cf1)
            elif float(cf1) < 100:
                cf1 = "0" + str(cf1)

            if float(sf2) < 10:
                sf2 = "0" + str(sf2)
            if float(cf2) < 10:
                cf2 = "00" + str(cf2)
            elif float(cf2) < 100:
                cf2 = "0" + str(cf2)

            # if len(cf1) == 1:
            #     cf1 = "00" + cf1
            # if len(cf1) == 2:
            #     cf1 = "0" + cf1

            # if len(sf2) == 1:
            #     sf2 = "0" + sf2
            # if len(cf2) == 1:
            #     cf2 = "00" + cf2
            # if len(cf2) == 2:
            #     cf2 = "0" + cf2

            # if float(sf1) < 10:
            #     sf1 = "0" + str(sf1)
            # if float(cf1) < 10:
            #     cf1 = "00" + str(cf1)
            # if float(cf1) < 100:
            #     cf1 = "0" + str(cf1)
            #
            # if float(sf2) < 10:
            #     sf2 = "0" + str(sf2)
            # if float(cf2) < 10:
            #     cf2 = "00" + str(cf2)
            # if float(cf2) < 100:
            #     cf2 = "0" + str(cf2)

            dest_fips = sf1 + str(cf1)

            ori_fips = str(sf2) + str(cf2)
            num_exemps = raw_df.iloc[j]['num_exemptions']
            # print(str(dest_fips) + " " + str(ori_fips))
            destination_fips.append(dest_fips)
            origin_fips.append(ori_fips)
            num_exemptions.append(num_exemps)

    d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
    df = pd.DataFrame(d)
    # print(df.head(5))
    migration_dfs[str(year)] = df
    print("year: " + str(year))
    print(migration_dfs[str(year)].head(5))
    print()
    year += 1

# NO FILE WITH NAME : ./migration_data/1213migrationdata/1213ny.xls
# NO FILE WITH NAME : ./migration_data/1314migrationdata/1314ut.xls
# NO FILE WITH NAME : ./migration_data/1314migrationdata/1314va.xls

print(list(migration_dfs.keys()))

# get num_cases for origin from std data[year]
# get total_pop for origin from census_data[year]
# divide num_cases by total_pop
# multiple num_exemps for this destination and origin from migration_dfs[year] to get the
    # number of infected people expected for this origin going to this county
# add up the expected_infected for destination (iterate over all their origins)
