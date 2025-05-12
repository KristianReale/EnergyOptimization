vE_SminPercentage(0).
vE_SmaxPercentage(100).
vDischargeMinPercentage(0).
vDischargeMaxPercentage(100).


vE_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMinPercentage(P).
vP_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMaxPercentage(P).
vE_Sinit(X) :- X = P * M / 100, maxChargeKWh(M), vE_SinitPercentage(P).




