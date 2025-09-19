vCharge(D, T, C) :- xP_S(D, I, C), C >= 0, time(I, T).
vCharge(D, T, 0) :- xP_S(D, I, C), C < 0, time(I, T).
vDischarge(D, T, -DIS) :- xP_S(D, I, DIS), DIS <= 0, time(I, T).
vDischarge(D, T, 0) :- xP_S(D, I, DIS), DIS > 0, time(I, T).

vFrom_grid(D, T, P_L - P_PV - DIS) :- time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, vDischarge(D, T, DIS).
vFrom_grid(D, T, 0) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L <= P_PV.

vFeed_in(D, T, P_PV - P_L - C) :- time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, vCharge(D, T, C).
vFeed_in(D, T, 0) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV <= P_L.

maxI(IMAX) :- IMAX = #max{I: time(I, T1)}.

vFinalCharge(X) :- maxI(IMAX), xE_S(_,IMAX,X).
vFinalChargePercentage(X) :- X = (P * 10000) / M, maxChargeKWh(M), vFinalCharge(P).


#show vP_L/3.
#show vP_PV/3.
#show vCharge/3.
#show vDischarge/3.
#show vFeed_in/3.
#show vFrom_grid/3.

#show vFinalChargePercentage/1.
#show vFinalCharge/1.
