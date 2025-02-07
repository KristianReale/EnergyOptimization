import pulp

def solve_optim(slots, storages_list, re_list, e_min_list, e_max_list, captotmin_list, captotmax_list, charging_tot, loads, productions):

    # Model
    prob = pulp.LpProblem(f"Min_problem", pulp.LpMinimize)

    # Variables 
    c_plus = [pulp.LpVariable.dicts("delivery_positive_part_t_{}".format(j+1), indices = range(slots),  lowBound = 0, cat=pulp.LpContinuous  ) for j in range(len(storages_list))] #aggiunta (energia assorbita dalla rete)
    c_minus = [pulp.LpVariable.dicts("delivery_negative_part_t_{}".format(j+1), indices = range(slots),  lowBound = 0, cat=pulp.LpContinuous  ) for j in range(len(storages_list))] #aggiunta (energia immessa in rete)

    s = [pulp.LpVariable.dicts("battery_load_t_{}".format(j+1), indices = range(slots),  lowBound = e_min_list[j],  upBound = e_max_list[j], cat=pulp.LpContinuous  ) for j in range(len(storages_list))]
    re = [pulp.LpVariable.dicts("battery_state_t_{storage}".format(storage=j+1), indices = range(slots + 1), lowBound = captotmin_list[j],  upBound = captotmax_list[j], cat=pulp.LpContinuous  ) for j in range(len(storages_list))]

    # componenti positive e negative
    s_plus = [pulp.LpVariable.dicts("battery_load_positive_part_t_{}".format(j+1), indices = range(slots),  lowBound = 0, cat=pulp.LpContinuous  ) for j in range(len(storages_list))] # energia accumulata nella batteria
    s_minus = [pulp.LpVariable.dicts("battery_load_negative_part_t_{}".format(j+1), indices = range(slots),  lowBound = 0, cat=pulp.LpContinuous  ) for j in range(len(storages_list))] # energia prelevata dalla batteria

    # Objective function
    prob += pulp.lpSum([ ( c_plus[j][i] + c_minus[j][i] + s_plus[j][i] + s_minus[j][i] ) for j in range(len(storages_list)) for i in range(slots)]), "Energy grid"

    for j in range(len(re_list)):
        prob += re[j][0] == re_list[j], "Battery_state_continuity_t_{}".format(j+1)

    for i in range(slots):

        for j in range(len(storages_list)):
            prob += re[j][i+1] == re[j][i] + (s_plus[j][i] - s_minus[j][i]), "NG{storage}_storage_constraint_t_{slot}".format(storage=j+1, slot=i+1)
            prob += s_plus[j][i] - s_minus[j][i] == s[j][i], "Total_s_{storage}_t_{slot}".format(storage=j+1, slot=i+1)
            prob += c_plus[j][i] - c_minus[j][i] == (loads[j][i] - productions[j][i]) + s[j][i], "Total_c_{storage}_t_{slot}".format(storage=j+1, slot=i+1) #aggiunta 

            prob += c_plus[j][i] <= loads[j][i] + s_plus[j][i] , "Total_c_plus_{storage}_t_{slot}".format(storage=j+1, slot=i+1) #aggiunta 
            prob += c_minus[j][i] <= productions[j][i] + s_minus[j][i] , "Total_c_minus_{storage}_t_{slot}".format(storage=j+1, slot=i+1) #aggiunta 

        prob += pulp.lpSum( s[j][i]  for j in range(len(storages_list)) ) == charging_tot[i], "Total_charging_t_{slot}".format(slot=i)


    prob.solve()
    print(pulp.LpStatus[prob.status])
    #print("The Min Value = ", pulp.value(prob.objective) )

    varsdict_new = {}
    for v in prob.variables():
        varsdict_new[v.name] = v.varValue

    return varsdict_new
