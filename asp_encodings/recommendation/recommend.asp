% Definizione fascia giorno
prev(I1, I) :- time(I, _), I1 = I-1, time(I1, _).
daytime(6..17).
nighttime(0..5).
nighttime(18..23).

% Luci alte solo di sera/notte e se produzione > consumi e batteria piena da almeno 1 ora e c’è ancora surplus
recommend(D, T, "lights_high") :- T = "11:00:00", date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
    socPercentage(I, SOCP), nighttime(I), prev(I1, I), socPercentage(I1, SOCP1).
%%recommend(D, T, "lights_low") :- T = "11:00:00", date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
%%    socPercentage(I, SOCP), daytime(I), prev(I1, I), socPercentage(I1, SOCP1).

soc(I, SOC + E_Sinit) :- time(I, T), SOC = #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).
socPercentage(I, SOCP) :-  SOCP = SOC * M / 10000, maxChargeKWh(M), soc(I, SOC).

% Luci basse se batteria scarica (<20%) o notte con poca produzione
%%recommend(H, "tieni le luci più basse") :-
%%    data(H,_,_,SOC), SOC < 20.
%%recommend(H, "tieni le luci più basse") :-
%%    data(H,P,C,_), nighttime(H), P < C.

#show recommend/3.
%#show soc/2.
%#show socPercentage/2.
%#show time/2.
%#show prev/2.
%#show vP_L/3.
%#show vP_PV/3.
