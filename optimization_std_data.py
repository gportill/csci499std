import pandas as pd


class County:
    def __init__(self, fips):
        self.fips = fips  # string
        self.neighbors = []
        self.year_to_cases_dict = {}  # {"year" : cases_for_year}
        self.year_to_pop_dict = {}  # {"year" : pop_for_year}
        self.year_to_mig_dict = {}  # {"year" : {dest_county:num_exemps, dest_count:num+exemps} }
        self.sum_cases_5_yr = 0

    def getFips(self):
        return self.fips

    def getSummedCases(self):
        return self.sum_cases_5_yr

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        # print(self.neighbors)

    def addCases(self, year, cases):
        # print(cases)
        if cases == 'Data not available':
            cases = "0"
        self.year_to_cases_dict[year] = int(cases.replace(",", ""))
        # print(self.year_to_cases_dict)

    def sumCases(self, cases):
        cases = cases.replace(",","")
        if cases == 'Data not available':
            print("SKIP", self.fips)
            cases = "0"
        self.sum_cases_5_yr += int(cases)

    def addPop(self, year, pop):
        self.year_to_pop_dict[year] = pop
        # print(self.year_to_pop_dict)

    def addMig(self, year, dict_of_destinations_to_num_exemps):
        self.year_to_mig_dict[year] = dict_of_destinations_to_num_exemps

    def isNeighborOf(self, fips):
        if fips in self.neighbors:
            return True
        return False


class ReadData:
    def __init__(self):
        self.county_to_fips_dict = {}
        # self.census_pop_total_dict = {}  # TODO maps YEAR to dictionary item of county:total_pop
        # self.mig_dest_ori_num_dict = {} # TODO maps destination county FIPS to dictionary item of origin:num_people_who_moved_to_destination
        self.fips_to_county_dict = {}

        self.il_fips = ['17001', '17003', '17005', '17007', '17009', '17011', '17013', '17015', '17017',
                        '17019', '17021', '17023', '17025', '17027', '17029', '17031', '17033',
                        '17035', '17037', '17039', '17041', '17043', '17045', '17047', '17049',
                        '17051', '17053', '17055', '17057', '17059', '17061', '17063', '17065',
                        '17067', '17069', '17071', '17073', '17075', '17077', '17079', '17081',
                        '17083', '17085', '17087', '17089', '17091', '17093', '17095', '17097',
                        '17099', '17101', '17103', '17105', '17107', '17109', '17111', '17113',
                        '17115', '17117', '17119', '17121', '17123', '17125', '17127', '17129',
                        '17131', '17133', '17135', '17137', '17139', '17141', '17143', '17145',
                        '17147', '17149', '17151', '17153', '17155', '17157', '17159', '17161',
                        '17163', '17165', '17167', '17169', '17171', '17173', '17175', '17177',
                        '17179', '17181', '17183', '17185', '17187', '17189', '17191', '17193',
                        '17195', '17197', '17199', '17201', '17203']

        self.nj_fips = ['34001', '34003', '34005', '34007', '34009', '34011', '34013', '34015', '34017',
                   '34019', '34021', '34023', '34025', '34027', '34029', '34031', '34033', '34035',
                   '34037', '34039', '34041']


    # gets data for the state's counties for 2012 to 2016 (most recent 6 years)
    # and adds up number of cases
    def read_std_data(self, state):  # state is 'il' or 'nj'
        if state == 'il':
            fips_for_state_counties = self.il_fips
        elif state == 'nj':
            fips_for_state_counties = self.nj_fips

        if state != 'nj' and state != 'il':
            print("Invalid state")
            return

        std_files = ["./chlam_data/2012_chlamydia.csv", "./chlam_data/2013_chlamydia.csv",
                     "./chlam_data/2014_chlamydia.csv", "./chlam_data/2015_chlamydia.csv",
                     "./chlam_data/2016_chlamydia.csv"]

        county_to_cases_count_dict = {}

        std_dfs = {}

        year = 2011

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
                curr_fips = str(currentLine[1]) + str(currentLine[2])
                if not curr_fips in fips_for_state_counties:
                    continue
                fips.append(str(currentLine[1]) + str(currentLine[2]))
                counties.append((str(currentLine[3]) + ", " + str(currentLine[0])).lower())
        # creating dictionary with county names and fips codes

        # fips_dict and self.county_to_fips_dict contain only the counties for specified state
        fips_dict = dict(zip(counties, fips))

        self.county_to_fips_dict = fips_dict
        # --------- End reading in all fips codes and associate them with county names --------

        # --------- Replace county names with FIPS codes in Geography column ---------
        for i in range(2012, 2017):
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

        df = std_dfs["2012"]
        for idx in range(0, len(std_dfs["2012"])):
            fips = df.iloc[idx]["Geography"]
            county_obj = County(fips)
            self.fips_to_county_dict[fips] = county_obj

        for i in range(2012, 2017):
            df = std_dfs[str(i)]
            for idx, val in df.iterrows():
                fips = df["Geography"][idx]
                cases = df["Cases"][idx]
                county_obj = self.fips_to_county_dict[fips]
                county_obj.addCases(str(i), cases)
                county_obj.sumCases(cases)

        # iterate through dictionary of fips to county_obj
        # save fips in one list
        # save sum_cases_5yr in another list
        # zip the two lists
        # save to excel

        summed_cases = []

        for fips_code in fips_for_state_counties:
            print(fips_code)
            county_obj = self.fips_to_county_dict[fips_code]
            sum_cases_5yr = county_obj.getSummedCases()
            summed_cases.append(sum_cases_5yr)

        # zip fips_for_state_counties and summed_cases

        summed_cases_data_for_df = {'fips': fips_for_state_counties, 'sum_cases_2012_2016': summed_cases}
        df = pd.DataFrame.from_dict(summed_cases_data_for_df)

        file = "./optimization_data/" + state + "_optimization_data_2012_2016.xlsx"

        df.to_excel(file, na_rep="nan", index=False)

        return std_dfs


rd = ReadData()
rd.read_std_data('il')
rd.read_std_data('nj')
