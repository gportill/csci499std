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
adj_fips_dict = rd.read_county_neighbors()
census_dfs = rd.read_census_data()
std_dfs = rd.read_std_data()
migration_dfs = rd.read_migration_data()

years = []
for i in range(2006, 2017):
    years.append(str(i))

# --------- below this line, working on calculating the migration feature for ONE year (2006) so that
    # it can later be turned into for loop over all years

i = 0
year = years[i]

census_df = census_dfs[year]
std_df = std_dfs[year]
mig_df = migration_dfs[year]

# Columns of data frames that are needed for the migration feature:
# census data: "Geo_FIPS", "SE_A00001_001" (total population is stored in SE_A00001_001)
# migration: destination, origin, num_exemps
# std: Geography, Cases
