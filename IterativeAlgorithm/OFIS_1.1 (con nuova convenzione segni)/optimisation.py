import pulp

def solve_optim(slots,p, q, over_p, under_p, cost_charge_1, cost_discharge_1, e_min_1, e_max_1, cap_tot_min_1, cap_tot_max_1, soc0_1, pun, pz, pap, pvp, creg_plus, creg_minus, poff_plus, poff_minus, e_min_seasonal_1, e_max_seasonal_1, cap_tot_min_seasonal_1, cap_tot_max_seasonal_1, soc0_seasonal_1, percentage_p_SEASONAL_1, percentage_m_SEASONAL_1):

    # Model

    model = pulp.LpProblem(f"Min_Cost_problem", pulp.LpMinimize)

    # Variables

    c_plus = pulp.LpVariable.dicts(
        name = 'delivery_positive_part',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    c_minus = pulp.LpVariable.dicts(
        name = 'delivery_negative_part',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    # accumulo giornaliero
    # litio
    s_1 = pulp.LpVariable.dicts(
        name = 'battery_load_1',
        indices = range(slots),
        lowBound = e_min_1,
        upBound = e_max_1,
        cat = pulp.LpContinuous
    )

    soc_1 = pulp.LpVariable.dicts(
        name = 'battery_state_1',
        indices = range(slots + 1),
        lowBound = cap_tot_min_1,
        upBound = cap_tot_max_1,
        cat = pulp.LpContinuous
    )

    # accumulo stagionale
    # idrogeno
    e_1 = pulp.LpVariable.dicts(
        name = 'seasonal_storage_load_1',
        indices = range(slots),
        lowBound = e_min_seasonal_1,
        upBound = e_max_seasonal_1,
        cat = pulp.LpContinuous
    )

    soc_seasonal_1 = pulp.LpVariable.dicts(
        name = 'battery_state_seasonal_1',
        indices = range(slots + 1),
        lowBound = cap_tot_min_seasonal_1,
        upBound = cap_tot_max_seasonal_1,
        cat = pulp.LpContinuous
    )

    # componenti positive e negative (accumulo giornaliero)
    # litio
    s_plus_1 = pulp.LpVariable.dicts(
        name = 'battery_load_positive_part_1',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    s_minus_1 = pulp.LpVariable.dicts(
        name = 'battery_load_negative_part_1',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    # componenti positive e negative (accumulo stagionale)
    # idrogeno
    e_plus_1 = pulp.LpVariable.dicts(
        name = 'seasonal_storage_load_positive_part_1',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    e_minus_1 = pulp.LpVariable.dicts(
        name = 'seasonal_storage_load_negative_part_1',
        indices = range(slots),
        lowBound = 0,
        cat = pulp.LpContinuous
    )

    # Objective function
    objective = pulp.lpSum([ ( (pun[i]) * c_plus[i]) - (pz[i] * c_minus[i]) + ( cost_charge_1 * s_plus_1[i] + cost_discharge_1 * s_minus_1[i] ) - (pap * e_plus_1[i]) + (pvp * e_minus_1[i]) - (poff_plus[i] * creg_plus[i]) - (poff_minus[i] * creg_minus[i])   for i in range(slots)])

    model += objective, "Cost"

    # Constraints
    # litio
    label0 = f"Battery_state_continuity_1"
    constraint0 = soc_1[0] == soc0_1
    model += constraint0, label0

    # idrogeno (stagionale)
    label2 = f"Battery_state_continuity_seasonal_1"
    constraint2 = soc_seasonal_1[0] == soc0_seasonal_1
    model += constraint2, label2

    for i in range(slots):

        label5 = f"Total_c[{i}]"
        constraint5 = c_plus[i] - c_minus[i] == (q[i] - p[i]) + (s_1[i]) + (e_1[i]) + (creg_plus[i]) - creg_minus[i] 
        model += constraint5, label5

        label6 = f"Positive_part_of_c[{i}]"
        constraint6 = c_plus[i] <= q[i] + creg_minus[i] 
        model += constraint6, label6

        label7 = f"Negative_part_of_c[{i}]"
        constraint7 = c_minus[i] <= p[i] + creg_plus[i]
        model += constraint7, label7

        #label11 = f"Service_minus[{i}]"
        #constraint11 = s_plus_1[i] - c_plus[i] >= creg_minus[i] 
        #model += constraint11, label11

        # litio
        label8 = f"Litium_storage_constraint_{i}"
        constraint8 = (
            soc_1[i+1] == soc_1[i] + (s_plus_1[i] - s_minus_1[i])
            )
        model += constraint8, label8

        # litio
        label9 = f"Negative_part_of_s_1[{i}]"
        constraint9 = s_plus_1[i] - s_minus_1[i] == s_1[i]
        model += constraint9, label9


        label12 = f"Seasonal_storage_constraint_1_{i}"
        constraint12 = (
            soc_seasonal_1[i+1] == soc_seasonal_1[i] + (e_plus_1[i] - e_minus_1[i])
            )
        model += constraint12, label12

        label13 = f"E_1_[{i}]"
        constraint13 = e_plus_1[i] - e_minus_1[i] == e_1[i]
        model += constraint13, label13

        label15 = f"Percentage_seasonal_over[{i}]"
        constraint15 = e_plus_1[i] <= over_p[i] * percentage_p_SEASONAL_1
        model += constraint15, label15

        label16 = f"Percentage_seasonal_under[{i}]"
        constraint16 = e_minus_1[i] <= under_p[i] * percentage_m_SEASONAL_1
        model += constraint16, label16


    model.solve()

    # PRINT MODEL STATUS
    print(pulp.LpStatus[model.status])

    # PRINT OPTIMAL SOLUTION
    print("The Min Value = ", pulp.value(model.objective) )

    varsdict = {}
    for v in model.variables():
        varsdict[v.name] = v.varValue
        #print(v.name, "=", v.varValue)

    return varsdict
