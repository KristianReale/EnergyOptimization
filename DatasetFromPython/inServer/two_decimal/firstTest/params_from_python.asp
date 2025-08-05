vGUESS(0..5000).
vE_SminPercentage(2000). % 20%
vE_SmaxPercentage(10000). % 100%
vDischargeMinPercentage(0).
%vDischargeMaxPercentage(10000).
vChargeMinPercentage(0).
%vChargeMaxPercentage(10000).


vE_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMinPercentage(P).
%vP_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMaxPercentage(P).
vP_Smax(1800).
vP_SminC(X) :- X = P * M / 10000, maxChargeKWh(M), vChargeMinPercentage(P).
%vP_SmaxC(X) :- X = P * M / 10000, maxChargeKWh(M), vChargeMaxPercentage(P).
vP_SmaxC(1800).

existsPrevCharge :- vFinalCharge(_).
vE_Sinit(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SinitPercentage(P), not existsPrevCharge.
vE_Sinit(X) :- vFinalCharge(X).



