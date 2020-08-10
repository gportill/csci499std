import gurobi as grb
import numpy as np
import pandas as pd
#import illinois_data_frames as id
import new_jersey_dataframes as nj
import pickle
import matplotlib.pyplot as plt

#census_tracts = fips data frame
#get number of infected for a given fips code
#number of predicted infected for each fips

read_data = pd.read_excel('optimization_data/nj_optimization_data_2012_2016.xlsx',   index_col=0).to_dict()
num_infected = read_data['sum_cases_2012_2016']

#could be FIPS codes, should be a LIST
census_tracts = list(num_infected.keys())

#dict of clinics per county (FIPS to number)
clinics_per_county_dict = nj.std_clinics_per_county
for tract in census_tracts:
    if str(tract) not in clinics_per_county_dict.keys():
        clinics_per_county_dict[str(tract)] = 0

#print("num infected keys list")
#print(num_infected.keys())

#takes adj dictionary that maps from fips to list of adj fips
# neighbor_list = nj.get_county_adjacency()
neighbor_list = pickle.load(open("nj_neighborlist.p", "rb"))
# pickle.dump(neighbor_list, open("nj_neighborlist.p", "wb"))
#make function in terms of budget (pass in budget, neighbor list, table of data)
def budget_func(budget, neighbor_list, census_tracts, minimum_coverage_tradeoff=1e100) :

    #create optimization model that will contain variables
    m = grb.Model("std_opt")

    #add decision variables
    #census tracks could be lookup_table.keys()
    num_constructed = m.addVars(census_tracts, vtype=grb.GRB.INTEGER, name="num_constructed")
    is_covered = m.addVars(census_tracts, vtype=grb.GRB.INTEGER, name="is_covered")

    # minimum_coverage = m.addVar(0, vtype=grb.GRB.CONTINUOUS, name="minimum_coverage")

    m.update()

    #loop through census tracks to add up total infected covered
    total_infected_covered = 0
    for tract in census_tracts:
        total_infected_covered += is_covered[tract] * num_infected[tract]

    #if multiple good soultions, chose buying fewer tracts
    #make number as small as possible
    m.setObjective(total_infected_covered
                   - 0.0001*sum(num_constructed[tract] for tract in census_tracts),
                   # + minimum_coverage_tradeoff*minimum_coverage,
                   sense=grb.GRB.MAXIMIZE)

    m.update()

    # need to pull in somewhere the actual data of where
    num_bought = 0
    for tract in census_tracts:
        num_bought += num_constructed[tract] - (clinics_per_county_dict[str(tract)] > 0)

    m.addConstr(num_bought <= budget, "construction budget")

    #loop through FIPS
    #for each FIP loop through neighbors
    # from IPython import embed
    # embed()
    for tract_1 in census_tracts:
        num_neighbors_bought = 0

       # print(tract_1)
       #  print(neighbor_list)
       # print(neighbor_list['01001'])
       # print(neighbor_list['17001'])
       # print(neighbor_list[str(tract_1)])
       # print(neighbor_list[tract_1.str()])
       # print(neighbor_list[tract_1].keys())

        for tract_2 in neighbor_list[str(tract_1)]:
            # print("this is tract 2")
            # print(tract_2)
            # print("this is is bought")
            # print(num_constructed)
            # print("this is is bought specific tract")
            # print(num_constructed[17009])
            tract_2_key = int(tract_2)
            if tract_2_key in census_tracts:
                num_neighbors_bought += num_constructed[int(tract_2)]

        m.addConstr(is_covered[tract_1] <= num_neighbors_bought, "adjacency_constraint")

    for tract in census_tracts:
        if clinics_per_county_dict[str(tract)] > 0:
            # clinics_per_county_dict[str(tract)]
            m.addConstr(num_constructed[tract] >= 1)
        m.addConstr(num_constructed[tract] <= (clinics_per_county_dict[str(tract)] + 2))

    # for tract in census_tracts:
    #     contrained_amount = is_covered[tract]/(num_infected[tract]+1)
    #     m.addConstr(minimum_coverage <= contrained_amount)

    m.update()

    m.optimize()

    #individual
    #num_constructed[FIPS].x
    print("objective:", m.objVal)

    print("optimal solution")
    for tract in census_tracts:
        print("{}: is bought {}".format(tract, num_constructed[int(tract)].x))
        print("{}: is covered {}".format(tract, is_covered[int(tract)].x))
    #print("minimum coverage:", minimum_coverage.x)
    print("total_infected_covered:", total_infected_covered.getValue())
    # from IPython import embed
    # embed()
    #return m.objVal, num_constructed, is_covered, total_infected_covered #, minimum_coverage
    return total_infected_covered.getValue()

#how many clinics we want to build
budget = []
infected_covered = []

for x in range(0, 30):
     infected_covered.append(budget_func(x, neighbor_list, census_tracts))
     budget.append(x)

plt.plot(budget, infected_covered, color='b')
plt.xlabel('Budget')
plt.ylabel('# of infected covered')
plt.show()