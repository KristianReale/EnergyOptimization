vE_SminPercentage(0).
vE_SmaxPercentage(10000).
vDischargeMinPercentage(0).
vDischargeMaxPercentage(10000).


vE_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMinPercentage(P).
vP_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMaxPercentage(P).
vE_Sinit(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SinitPercentage(P).




