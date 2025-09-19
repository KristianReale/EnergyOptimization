vGUESS(0..322).
vE_SminPercentage(200). % 20%
vE_SmaxPercentage(1000). % 100%
vDischargeMinPercentage(0).
%vDischargeMaxPercentage(1000).
vChargeMinPercentage(0).
%vChargeMaxPercentage(1000).


vE_Smin(X) :- X = P * M / 1000, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 1000, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 1000, maxChargeKWh(M), vDischargeMinPercentage(P).
%vP_Smax(X) :- X = P * M / 1000, maxChargeKWh(M), vDischargeMaxPercentage(P).
vP_Smax(500).
vP_SminC(X) :- X = P * M / 1000, maxChargeKWh(M), vChargeMinPercentage(P).
%vP_SmaxC(X) :- X = P * M / 1000, maxChargeKWh(M), vChargeMaxPercentage(P).
vP_SmaxC(500).

existsPrevCharge :- vFinalCharge(_).
vE_Sinit(X) :- X = P * M / 1000, maxChargeKWh(M), vE_SinitPercentage(P), not existsPrevCharge.
vE_Sinit(X) :- vFinalCharge(X).



