vE_SminPercentage(5).
vE_SmaxPercentage(100).
vDischargeMinPercentage(0).
vDischargeMaxPercentage(100).
maxChargeKWh(1000).

vE_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMinPercentage(P).
vP_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMaxPercentage(P).
vE_Sinit(X) :- X = P * M / 100, maxChargeKWh(M), vE_SinitPercentage(P).


%buyMore("2020-01-01", "2:15", 350).
%buyMore("2020-01-01", "9:0", 450).
%buyMore("2020-01-01", "12:45", 20).
%buyMore("2020-01-01", "21:30", 200).




