import read_data

# for a particular year
    # for each row of STD data: => county i (for each row, we will look at county i's neighbors in migration data)
        # store the county's neighbors in a list (available in adj_fips_dict)
        # initialize expected_infected = 0
        # for each neighbor j in the list:
            # find neighbor j's migration rate to county i in mig_dfs for this year
            # find neighbor j's total pop in census data for this year
            # find neighbor's std cases in std data for this year
            # expected_infected = calculate std_cases / total_pop * mig_rate
            # add that calculation to the expected_infected variable (so you are adding up expected_infected for all of their neighbors). this number will be the feature in the end.

rd = read_data.ReadData()
print("reading read_std_data")
std_dfs = rd.read_std_data()
print("reading adj_fips_dict")
adj_fips_dict = rd.read_county_neighbors()
print("reading census_data")
census_dfs = rd.read_census_data()
print("before migration_dfs")
migration_dfs = rd.read_migration_data()
print("after migration_dfs")
fips_to_county_dict = rd.get_fips_to_county_dict()

years = []
for i in range(2006, 2017):
    years.append(str(i))

# --------- below this line working on creating infected migration map inflow for all years

year_to_county_to_STD_inflows = {}

#for each year
for i in range(2006,2017):
    mig_df = migration_dfs[str(i)]
    std_df = std_dfs[str(i)]
    census_df = census_dfs[str(i)]
    census_total_pop_column = 'SE_A00001_001' 
    dest_to_inflow = {}
    #for each county
    for destination in fips_to_county_dict.keys():
        total_infected_inflow = 0
        #for each neighbor
        for origin in fips_to_county_dict[destination].neighbors:
            #calculate infected inflow from this neighbor
            #get cases of infection
            case_rows = std_df[std_df["Geography"] == origin]["Cases"]
            if len(case_rows) == 0:
                cases = '0'
            else:
                cases = std_df[std_df["Geography"] == origin]["Cases"].item()
            #get the population
            pop_rows = census_df[census_df["Geo_FIPS"] == origin]
            if len(pop_rows) == 0:
                pop = '0'
            else:
                pop = census_df[census_df["Geo_FIPS"] == origin][census_total_pop_column].item()
            #calculate ratio
            if float(pop.replace(",", "")) == 0:
                infected_ratio = 0
            else:
                infected_ratio = float(cases.replace(",", ""))/float(pop.replace(",", ""))
            # ratio * num migrating to dest = infected flow 
            num_exemp_rows = mig_df[(mig_df["destination"] == destination) & (mig_df["origin"] == origin)]["num_exemps"]
            if len(num_exemp_rows) == 0:
                num_exemps = 0;
            else:
                num_exemps = float(mig_df[(mig_df["destination"] == destination) & (mig_df["origin"] == origin)]["num_exemps"].item())
            infected_flow = infected_ratio * num_exemps
            total_infected_inflow += infected_flow
        #add total to dictionary
        dest_to_inflow[destination] = total_infected_inflow
    #add dictionary to dictionary
    year_to_county_to_STD_inflows[str(i)] = dest_to_inflow


# --------- below this line, working on calculating the migration feature for ONE year (2006) so that
    # it can later be turned into for loop over all years

# i = 0
# year = years[i]

# census_df = census_dfs[year]
# std_df = std_dfs[year]
# mig_df = migration_dfs[year]

# census_total_pop_column = 'SE_A00001_001' 

# infected_ratio = {}
# # iterate over census tracts
# for tract_id in census_df["Geo_FIPS"]:
#     # get the number of cases for the current geography
#     case_rows = std_df[std_df["Geography"] == tract_id]["Cases"]
#     if len(case_rows) == 0:
#         cases = '0'
#     else:
#         cases = std_df[std_df["Geography"] == tract_id]["Cases"].item()
#     #get the population
#     pop = census_df[census_df["Geo_FIPS"] == tract_id][census_total_pop_column].item()
#     print(pop)
    #calculate ratio
#     infected_ratio[tract_id] = float(cases.replace(",", ""))/float(pop.replace(",", ""))


# # temporary code, not tested with dataset yet
# migration_infected = {} # maps geo_FIPS to number of entering infected
# assuming that migration data is a list of tuples (source, dest, count)
# d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
# i.e. formatted_migration_data = mig_df
# formatted_migration_data = mig_df
# for row in formatted_migration_data.iterrows():
#     dest = row[0] #"destination"
#     origin = row[1] #"origin"
#     count = float(row[2].replace(",","")) #"num_exemps"
#     infected_inflow = infected_ratio[origin]*count
#     if dest not in migration_infected:
#         migration_infected[dest] = 0
#     migration_infected[dest] += infected_inflow





# Columns of data frames that are needed for the migration feature:
# census data: "Geo_FIPS", "SE_A00001_001" (total population is stored in SE_A00001_001)
# migration: destination, origin, num_exemps
# std: Geography, Cases

census_df[census_df["Geo_FIPS"] == 1001]["SE_A00001_001"].item()