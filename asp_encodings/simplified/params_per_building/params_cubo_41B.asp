vGUESS(0..1600).
vDischargeMinPercentage(0).
%vDischargeMaxPercentage(10000).
vChargeMinPercentage(0).
%vChargeMaxPercentage(10000).



%UNICAL
%minimo 5%
%unical max 16kw cubo 18B
%unical max 32kw cubo 41B


vE_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SmaxPercentage(P).
vP_Smin(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMinPercentage(P).
%vP_Smax(X) :- X = P * M / 10000, maxChargeKWh(M), vDischargeMaxPercentage(P).
vP_Smax(1600).
vP_SminC(X) :- X = P * M / 10000, maxChargeKWh(M), vChargeMinPercentage(P).
%vP_SmaxC(X) :- X = P * M / 10000, maxChargeKWh(M), vChargeMaxPercentage(P).
vP_SmaxC(1600).

existsPrevCharge :- vFinalCharge(_).
vE_Sinit(X) :- X = P * M / 10000, maxChargeKWh(M), vE_SinitPercentage(P), not existsPrevCharge.
vE_Sinit(X) :- vFinalCharge(X).



