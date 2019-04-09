import pandas as pd
from pathlib import Path

class County:
    def __init__(self, fips):
        self.fips = fips  # string
        self.neighbors = []
        self.year_to_cases_dict = {}  # {"year" : cases_for_year}
        self.year_to_pop_dict = {}  # {"year" : pop_for_year}
        self.year_to_mig_dict = {}  # {"year" : {dest_county:num_exemps, dest_count:num+exemps} }

    def getFips(self):
        return self.fips

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        # print(self.neighbors)

    def addCases(self, year, cases):
        # print(cases)
        if cases == 'Data not available':
            cases = "0"
        self.year_to_cases_dict[year] = int(cases.replace(",", ""))
        # print(self.year_to_cases_dict)

    def addPop(self, year, pop):
        self.year_to_pop_dict[year] = pop
        # print(self.year_to_pop_dict)

    def addMig(self, year, dict_of_destinations_to_num_exemps):
        self.year_to_mig_dict[year] = dict_of_destinations_to_num_exemps

    def isNeighborOf(self, fips):
        if fips in self.neighbors:
            return True
        return False

## -------- IMPORTANT: When using this class, call the functions in this order:
## 1. read_std_data
## 2. read_county_neighbors
## 3. read_census_data
## 4. migration_data
## 5. get_fips_to_county_dict

class ReadData:
    def __init__(self):
        self.county_to_fips_dict = {}
        # self.census_pop_total_dict = {}  # TODO maps YEAR to dictionary item of county:total_pop
        # self.mig_dest_ori_num_dict = {} # TODO maps destination county FIPS to dictionary item of origin:num_people_who_moved_to_destination
        self.fips_to_county_dict = {}

    def get_fips_to_county_dict(self):
        return self.fips_to_county_dict

    def read_census_data(self):
        census_files = ["./census_data/2006_census_with_total_pop.csv", "./census_data/2007_census_with_total_pop.csv",
                        "./census_data/2008_census_with_total_pop.csv", "./census_data/2009_census_with_total_pop.csv",
                        "./census_data/2010_census_with_total_pop.csv", "./census_data/2011_census_with_total_pop.csv",
                        "./census_data/2012_census_with_total_pop.csv", "./census_data/2013_census_with_total_pop.csv",
                        "./census_data/2014_census_with_total_pop.csv", "./census_data/2015_census_with_total_pop.csv",
                        "./census_data/2016_census_with_total_pop.csv"]

        census_dfs = {}

        year = 2005

        for file in census_files:
            year += 1
            key = str(year)
            census_dfs[key] = pd.read_csv(file, encoding='latin-1', index_col=False, dtype=str)

        cols_to_keep = {"Geo_FIPS": "fips",
                "SE_A00001_001": "total_pop",
                "SE_A00002_001": "pop_density",
                "SE_A02001_002": "male",
                "SE_A02001_003": "female",
                "SE_A01001_002": "age_under5",
                "SE_A01001_003": "age_5_to_9",
                "SE_A01001_004": "age_10_to_14",
                "SE_A01001_005": "age_15_to_17",
                "SE_A01001_006": "age_18_to_24",
                "SE_A01001_007": "age_25_to_34",
                "SE_A01001_008": "age_35_to_44",
                "SE_A01001_009": "age_45_to_54",
                "SE_A01001_010": "age_55_to_64",
                "SE_A01001_011": "age_65_to_74",
                "SE_A01001_012": "age_75_to_84",
                "SE_A01001_013": "age_85older",
                "SE_A03001_002": "race_white_alone",
                "SE_A03001_003": "race_black",
                "SE_A03001_004": "race_american_indian_alaska_native_alone",
                "SE_A03001_005": "race_asian_alone",
                "SE_A03001_006": "race_native_hawaiian",
                "SE_A03001_007": "race_other_race_alone",
                "SE_A03001_008": "race_two_races",
                "SE_A04001_002": "not_hispanic_total",
                "SE_A04001_003": "not_hispanic_white_alone",
                "SE_A04001_004": "not_hispanic_black",
                "SE_A04001_005": "not_hispanic_american_indian",
                "SE_A04001_006": "not_hispanic_asian_alone",
                "SE_A04001_007": "not_hispanic_native_hawaiian",
                "SE_A04001_008": "not_hispanic_other_race_alone",
                "SE_A04001_009": "not_hispanic_two_races",
                "SE_A04001_010": "hispanic_total",
                "SE_A04001_011": "hispanic_white_alone",
                "SE_A04001_012": "hispanic_black",
                "SE_A04001_013": "hispanic_american_indian",
                "SE_A04001_014": "hispanic_asian_alone",
                "SE_A04001_015": "hispanic_native_hawaiian",
                "SE_A04001_016": "hispanic_other_race_alone",
                "SE_A04001_017": "hispanic_two_races",
                "SE_A10003_001": "avg_household_size",
                "SE_A11001_001": "pop_15_and_older",
                "SE_A11001_002": "never_married",
                "SE_A11001_003": "now_married",
                "SE_A11001_004": "separated",
                "SE_A11001_005": "widowed",
                "SE_A11001_006": "divorced",
                "SE_A12002_002": "edu_attainment_less_than_high_school",
                "SE_A12002_003": "edu_attainment_high_school_grad",
                "SE_A12002_004": "edu_attainment_some_college",
                "SE_A12002_005": "edu_attainment_bach_degree",
                "SE_A12002_006": "edu_attainment_masters_degree",
                "SE_A12002_007": "edu_attainment_professional_school_degree",
                "SE_A12002_008": "edu_attainment_doctorate_degree",
                "SE_A12003_002": "school_dropout_16_to_19_not_hs_graduate",
                "SE_A12003_003": "school_dropout_hs_graduate",
                "SE_A17002_002": "employment_status_16_plus_IN_labor_force",
                "SE_A17002_003": "employment_status_16_plus_in_armed_forces",
                "SE_A17002_004": "employment_status_16_plus_civilian",
                "SE_A17002_005": "employment_status_16_plus_civilian_employed",
                "SE_A17002_006": "employment_status_16_plus_civilian_unemployed",
                "SE_A17002_007": "employment_status_16_plus_not_in_labor_force",
                "SE_A17005_002": "employment_rate",
                "SE_A17005_003": "unemployment_rate",
                "SE_A14001_002": "household_income_less_than_10000",
                "SE_A14001_003": "household_income_10_to_15",
                "SE_A14001_004": "household_income_15_to_20",
                "SE_A14001_005": "household_income_20_to_25",
                "SE_A14001_006": "household_income_25_to_30",
                "SE_A14001_007": "household_income_30_to_35",
                "SE_A14001_008": "household_income_35_to_40",
                "SE_A14001_009": "household_income_40_to_45",
                "SE_A14001_010": "household_income_45_to_50",
                "SE_A14001_011": "household_income_50_to_60",
                "SE_A14001_012": "household_income_60_to_75",
                "SE_A14001_013": "household_income_75_to_100",
                "SE_A14001_014": "household_income_100_to_125",
                "SE_A14001_015": "household_income_125_to_140",
                "SE_A14001_016": "household_income_150_to_200",
                "SE_A14001_017": "household_income_over_200",
                "SE_A13002_002": "poverty_status_12mo_families_with_income_below_poverty_level",
                "SE_A13002_003": "poverty_status_12mo_family_type_married_with_children",
                "SE_A13002_004": "poverty_status_12mo_family_type_married_no_children",
                "SE_A13002_006": "poverty_status_12mo_family_type_malehouseholder_nowife_with_children",
                "SE_A13002_007": "poverty_status_12mo_family_type_malehouseholder_nowife_no_children",
                "SE_A13002_009": "poverty_status_12mo_family_type_femalehouseholder_nohusband_with_children",
                "SE_A13002_010": "poverty_status_12mo_family_type_num_",
                "SE_A13002_011": "poverty_status_12mo_family_type_num",
                "SE_A13003A_002": "poverty_status_under18_living_in_poverty",
                "SE_A13003B_002": "poverty_status_18_to_64_living_in_poverty",
                "SE_A13003C_002": "poverty_status_65older_living_in_poverty",
                "SE_A13001A_002": "poverty_status_white_alone_below_poverty_level",
                "SE_A13001B_002": "poverty_status_black_alone_below_poverty_level"}

        vars_to_code = {v: k for k, v in cols_to_keep.items()}

        col_keys = list(cols_to_keep.keys())

        census_dfs_cond = {}  # all the census data we need (no health insurance)
        for year in range(2006, 2017):
            year_str = str(year)
            curr_df = census_dfs[year_str]
            new_df = curr_df[col_keys]
            census_dfs_cond[year_str] = new_df

        for i in range(2006, 2017):
            df = census_dfs_cond[str(i)]
            for idx, val in df.iterrows():
                fips = df["Geo_FIPS"][idx]
                pop = df["SE_A00001_001"][idx]
                # print("type of stcd in census: " + str(type(self.fips_to_county_dict)))

                if fips in self.fips_to_county_dict.keys():
                    county_obj = self.fips_to_county_dict[fips]
                    # print("type of CO in census: " + str(type(county_obj)))
                    # ****Why does county_obj come back as a list??
                    # print(county_obj)
                    # print("COUNTY OBJ: " + ''.join(county_obj))  ###
                    county_obj.addPop(str(i), pop)
                else:
                    print("cannot add population information to county " + fips + " for year " + str(i))
        # for i in range(2006, 2017):
        #     df = std_dfs[str(i)]
        #     for idx, val in df.iterrows():
        #         fips = df["Geography"][idx]
        #         cases = df["Cases"][idx]
        #         county_obj = self.fips_to_county_dict[fips]
        #         county_obj.addCases(str(i), cases)
        return census_dfs_cond

    def read_std_data(self):
        std_files = ["./chlam_data/2006_chlamydia.csv", "./chlam_data/2007_chlamydia.csv",
                     "./chlam_data/2008_chlamydia.csv",
                     "./chlam_data/2009_chlamydia.csv", "./chlam_data/2010_chlamydia.csv",
                     "./chlam_data/2011_chlamydia.csv",
                     "./chlam_data/2012_chlamydia.csv", "./chlam_data/2013_chlamydia.csv",
                     "./chlam_data/2014_chlamydia.csv",
                     "./chlam_data/2015_chlamydia.csv", "./chlam_data/2016_chlamydia.csv"]

        std_dfs = {}

        year = 2005

        for file in std_files:
            year += 1
            key = str(year)
            std_dfs[key] = pd.read_csv(file, encoding='latin-1')
            # (std_dfs[key].head(5))

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
        self.county_to_fips_dict = fips_dict
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
                    to_drop.append(df["Geography"][idx])

            # dropping the county names with no fips code
            for x in to_drop:
                df = df[df.Geography != x]
        # --------- End replacing county names with FIPS codes in Geography column ---------

        df = std_dfs["2006"]
        for idx in range(0, len(std_dfs["2006"])):
            fips = df.iloc[idx]["Geography"]
            county_obj = County(fips)
            self.fips_to_county_dict[fips] = county_obj

        for i in range(2006, 2017):
            df = std_dfs[str(i)]
            for idx, val in df.iterrows():
                fips = df["Geography"][idx]
                cases = df["Cases"][idx]
                county_obj = self.fips_to_county_dict[fips]
                county_obj.addCases(str(i), cases)

        return std_dfs

    def read_migration_data(self):
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
                if i == 0:
                    file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[i] + state + "i.xls"
                elif i == 1:
                    state_name = state.lower()
                    state_name = state_name.capitalize()
                    file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[
                        i] + state_name + "i.xls"
                elif i == 2 or i == 3:
                    state_name = state.lower()
                    state_name = state_name.capitalize()
                    file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[
                        i] + "i" + state + ".xls"
                elif i == 4:
                    file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[
                        i] + "i" + state + ".xls"
                elif i == 5:
                    state_name = state.lower()
                    file = "./migration_data/" + year_codes[i] + "migrationdata/co" + year_codes[
                        i] + "i" + state_name + ".xls"

                raw_df = pd.read_excel(file, encoding="ISO-8859-1")
                col_names = ["state_fips1", "county_fips1", "state_fips2", "county_fips2", "state", "description",
                             "num_returns",
                             "num_exemptions", "agg_adj_gross_income"]

                raw_df = pd.read_excel(file, encoding="ISO-8859-1", skiprows=8, header=None, names=col_names, dtype=str)
                raw_df = raw_df[~raw_df.description.str.contains("Total", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Other", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Tot", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Foreign", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Non-Migrants", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Non-Migrant", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Non-migrants", na=False)]
                raw_df = raw_df[~raw_df.description.str.contains("Non-migrant", na=False)]

                for j in range(0, len(raw_df)):
                    dest_fips = str(raw_df.iloc[j]['state_fips1']) + str(raw_df.iloc[j]['county_fips1'])
                    ori_fips = str(raw_df.iloc[j]['state_fips2']) + str(raw_df.iloc[j]['county_fips2'])
                    num_exemps = raw_df.iloc[j]['num_exemptions']
                    destination_fips.append(dest_fips)
                    origin_fips.append(ori_fips)
                    num_exemptions.append(num_exemps)

            d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
            df = pd.DataFrame(d)
            migration_dfs[str(year)] = df
            year += 1

        ########## now read 2011-2012 files ##########

        year_codes = ["1112", "1213", "1314", "1415", "1516"]
        year = 2012

        for i in range(0, 5):  # 1112 to 1516
            # xls = pd.ExcelFile('path_to_file.xls')
            destination_fips = []
            origin_fips = []
            num_exemptions = []

            for state in state_abbrev:
                state_name = state.lower()
                file = "./migration_data/" + year_codes[i] + "migrationdata/" + year_codes[i] + state_name + ".xls"
                config = Path(file)
                if not config.is_file():
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


                for j in range(0, len(raw_df)):
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

                    dest_fips = sf1 + str(cf1)

                    ori_fips = str(sf2) + str(cf2)
                    num_exemps = raw_df.iloc[j]['num_exemptions']
                    destination_fips.append(dest_fips)
                    origin_fips.append(ori_fips)
                    num_exemptions.append(num_exemps)

            d = {'destination': destination_fips, 'origin': origin_fips, 'num_exemps': num_exemptions}
            df = pd.DataFrame(d)
            migration_dfs[str(year)] = df
            year += 1

        # NO FILE WITH NAME : ./migration_data/1213migrationdata/1213ny.xls
        # NO FILE WITH NAME : ./migration_data/1314migrationdata/1314ut.xls
        # NO FILE WITH NAME : ./migration_data/1314migrationdata/1314va.xls

        return migration_dfs

    def read_county_neighbors(self):
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

        ### make fips adj dictionary ###

        curr_county = str(county_adj_df.iloc[0, fips_col])
        neighbors = []

        for i in range(1, len(county_adj_df)):
            if not pd.isnull(county_adj_df.iloc[i, fips_col]) and i > 1:  # new_county
                # add current list to old_county in dictionary
                fips_adj_dict[curr_county] = neighbors
                if curr_county in self.fips_to_county_dict.keys():
                    county_obj = self.fips_to_county_dict[curr_county]
                    county_obj.setNeighbors(neighbors)
                else:
                    print("No std info for county " + curr_county + " so cannot add neighbors to county with that fips")
                neighbors = []
                curr_county = str(county_adj_df.iloc[i, fips_col])
            else:
                neighbors.append(str(county_adj_df.iloc[i, neighbor_fips_col]))

        return fips_adj_dict
