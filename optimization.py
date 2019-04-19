import gurobi as grb
import numpy as np
import pandas as pd
import illinois_data_frames

#set up data, in this example it's random
#census_tracts = fips data frame
#get number of infected for a given fips code
#number of predicted infected for each fips

budget = 1
# num_census_tracts = 30
# num_infected = np.random.rand(num_census_tracts)

read_data = pd.read_excel("illinois_data/illinois_2006_cpp.xlsx",   index_col=0).to_dict()
num_infected = read_data['target_t5']

#could be FIPS codes, should be a LIST
census_tracts = list(num_infected.keys())

neighbor_list= illinois_data_frames.get_county_adjacency()
#neighbor_list = {t:np.random.choice(census_tracts, 5) for t in census_tracts}

#for is_neighbor take adj dictionary that maps from fips to list of adj fips

#make function in terms of budget (pass in budget, neighbor list, table of data)


#create optimization model that will contain variables
m = grb.Model("std_opt")

#add decision variables
#census tracks could be lookup_table.keys()
is_bought = m.addVars(census_tracts, vtype=grb.GRB.BINARY, name="is_bought")
is_covered = m.addVars(census_tracts, vtype=grb.GRB.BINARY, name="is_covered")

m.update()

#loop through census tracks to add up total infected covered
total_infected_covered = 0
for tract in census_tracts:
    total_infected_covered += is_covered[tract] * num_infected[tract]

#if multiple good soultions, chose buying fewer tracts
#make number as small as possible
m.setObjective(total_infected_covered - 0.0001*sum(is_bought[tract] for tract in census_tracts), sense=grb.GRB.MAXIMIZE)

m.update()

num_bought = 0
for tract in census_tracts:
    num_bought += is_bought[tract]

m.addConstr(num_bought <= budget, "construction budget")

for tract_1 in census_tracts:
    num_neighbors_bought = 0
    # for tract_2 in census_tracts:
    #     num_neighbors_bought += is_bought[tract_2] * is_neighbor[tract_1, tract_2]

    #what we will do
    for tract_2 in neighbor_list[tract_1]:
       num_neighbors_bought += is_bought[tract_2]
    # num_neighnors_bought += is_bought{tract_1]

    m.addConstr(is_covered[tract_1] <= num_neighbors_bought, "adjacency_constraint")

m.update()
m.optimize()

#individual
#is_bought[FIPS].x

print("optimal solution")
for tract in census_tracts:
    print("{}: is bought {}".format(tract, is_bought[tract].x))
    print("{}: is covered {}".format(tract, is_covered[tract].x))