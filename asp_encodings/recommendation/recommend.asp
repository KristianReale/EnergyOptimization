% Definizione fascia giorno
prev(I1, I) :- time(I, _), I1 = I-1, time(I1, _).
daytime(6..17).
nighttime(0..5).
nighttime(18..23).
%timeTarget("23:00:00").

soc(I, SOC + E_Sinit) :- time(I, T), SOC = #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).
socPercentage(I, SOCP) :-  SOCP = SOC * 10000 / M, maxChargeKWh(M), soc(I, SOC).

% Luci alte solo di sera/notte e se produzione > consumi e batteria piena da almeno 1 ora e c’è ancora surplus
recommend(D, T, "lights_high") :- timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), nighttime(I), prev(I1, I), soc(I1, SOC1), |SOC - SOC1| < 1000,  P_L - P_PV < 500.
recommend(D, T, "lights_low") :- timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), daytime(I), prev(I1, I), soc(I1, SOC1), |SOC - SOC1| < 1000.

recommend(D, T, "temp_high") :- timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), nighttime(I), prev(I1, I), soc(I1, SOC1), |SOC - SOC1| < 1000,  P_L - P_PV < 500.
recommend(D, T, "temp_low") :- timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), daytime(I), prev(I1, I), soc(I1, SOC1), |SOC - SOC1| < 1000.

recommend(D, T, "dicharge") :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, timeTarget(T), time(I, T), socPercentage(I, SOCP), SOCP > EMINP, vE_SminPercentage(EMINP).
recommend(D, T, "charge") :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L < P_PV, timeTarget(T), time(I, T), socPercentage(I, SOCP), SOCP < EMAXP, vE_SmaxPercentage(EMAXP).

#show recommend/3.
%#show soc/2.
#show socPercentage/2.
#show soc/2.
#show time/2.
%#show prev/2.
%#show vP_L/3.
%#show vP_PV/3.
#show vE_Sinit/1.
