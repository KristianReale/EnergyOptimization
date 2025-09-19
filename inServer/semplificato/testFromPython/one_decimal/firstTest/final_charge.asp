maxI(IMAX) :- IMAX = #max{I: time(I, T1)}.
vFinalCharge(X + E_Sinit) :- maxI(IMAX), I = IMAX, time(I, T1), X = #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).

vFinalChargePercentage(X) :- X = (P * 1000) / M, maxChargeKWh(M), vFinalCharge(P).
#show vFinalChargePercentage/1.
#show vFinalCharge/1.


