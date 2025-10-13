vGUESSMAX(18).
vE_SminPercentage(5). % 5%
vE_SmaxPercentage(100). % 100%
vDischargeMinPercentage(0).
%vDischargeMaxPercentage(10000).
vChargeMinPercentage(0).
%vChargeMaxPercentage(10000).

vE_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vE_SminPercentage(P).
vE_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vE_SmaxPercentage(P).

vP_Smin(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMinPercentage(P).
%vP_Smax(X) :- X = P * M / 100, maxChargeKWh(M), vDischargeMaxPercentage(P).
vP_Smax(18).
vP_SminC(X) :- X = P * M / 100, maxChargeKWh(M), vChargeMinPercentage(P).
%vP_SmaxC(X) :- X = P * M / 100, maxChargeKWh(M), vChargeMaxPercentage(P).
vP_SmaxC(18).

existsPrevCharge :- vFinalCharge(_).
vE_Sinit(X) :- X = P * M / 100, maxChargeKWh(M), vE_SinitPercentage(P), not existsPrevCharge.

%UNICAL
%minimo 5%
%unical max 16kw cubo 18B
%unical max 32kw cubo 41B



