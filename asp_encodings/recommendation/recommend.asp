% Definizione fascia giorno
prev(I1, I) :- time(I, _), I1 = I-1, time(I1, _).
daytime(6..18).
nighttime(1..5).
nighttime(19..24).

%timeTarget("23:00:00").

soc(I, SOC + E_Sinit) :- time(I, T), SOC = #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).
socPercentage(I, SOCP) :-  SOCP = SOC * 10000 / M, maxChargeKWh(M), soc(I, SOC).

% Se durante la notte la potenza richiesta è vicina a quella prodotta dal fotovoltaico, lo stato di carica della batteria non diminuisce significativamente rispetto all’istante precedente, il deficit energetico è contenuto e non c’è stato prelievo di energia dalla rete nel passo temporale precedente, il sistema raccomanda di aumentare l’illuminazione.
recommend(D, T, "lights_high") :- nighttime(I),
    timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), SOC <= SOC_PREV, SOC_PREV - SOC < 500, |P_L - P_PV| < 500, vFrom_grid(D, T_PREV, F), time(I_PREV, T_PREV), F = 0.

% Se durante il giorno la potenza richiesta supera quella prodotta dal fotovoltaico, il deficit è contenuto (inferiore a 500), lo stato di carica della batteria rimane stabile rispetto all’istante precedente e c’è stato acquisto di energia dalla rete nel passo temporale precedente, il sistema raccomanda di abbassare le luci.
recommend(D, T, "lights_low") :- daytime(I),
    timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), |SOC - SOC_PREV| < 1000, P_L - P_PV < 500, vFrom_grid(D, T_PREV, F), time(I_PREV, T_PREV), F > 0.

% Se in inverno, durante il giorno, la potenza richiesta è vicina a quella prodotta dal fotovoltaico, lo stato di carica della batteria non diminuisce significativamente rispetto all’istante precedente, il deficit energetico è contenuto e non c’è stato prelievo di energia dalla rete nel passo temporale precedente, il sistema raccomanda di aumentare la temperatura.
recommend(D, T, "temp_high") :- season(winter), daytime(I),
    timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), SOC <= SOC_PREV, SOC_PREV - SOC < 500, |P_L - P_PV| < 500, vFrom_grid(D, T_PREV, F), time(I_PREV, T_PREV), F = 0.

% Se in inverno, durante la notte, la potenza richiesta è vicina a quella prodotta dal fotovoltaico e lo stato di carica della batteria non diminuisce significativamente rispetto all’istante precedente, il sistema raccomanda di aumentare la temperatura.
recommend(D, T, "temp_high") :- season(winter), nighttime(I), timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), SOC <= SOC_PREV, SOC_PREV - SOC < 500, |P_L - P_PV| < 500.

% Se è estate e durante la notte la potenza richiesta supera quella prodotta dal fotovoltaico con un deficit elevato, mentre lo stato di carica della batteria non diminuisce significativamente rispetto all’istante precedente, il sistema raccomanda di aumentare la temperatura.
recommend(D, T, "temp_high") :- season(summer), nighttime(I), timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),  P_L > P_PV,
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), SOC <= SOC_PREV, SOC_PREV - SOC < 500, P_L - P_PV > 500.

% Se in inverno, durante il giorno, la potenza richiesta supera quella prodotta dal fotovoltaico con un deficit elevato, lo stato di carica della batteria resta stabile e vi è stato prelievo di energia dalla rete nel passo temporale precedente, il sistema raccomanda di abbassare la temperatura.
recommend(D, T, "temp_low") :- season(winter), daytime(I), timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV,
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), |SOC - SOC_PREV| < 1000, P_L - P_PV > 500, vFrom_grid(D, T_PREV, F), time(I_PREV, T_PREV), F > 0.

% Se è estate e durante il giorno la potenza richiesta è simile a quella prodotta dal fotovoltaico, lo stato di carica della batteria resta stabile e non c’è stato prelievo di energia dalla rete nel passo temporale precedente, il sistema raccomanda di abbassare la temperatura.
recommend(D, T, "temp_low") :- season(summer), daytime(I), timeTarget(T), date(D), time(I, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV),
    soc(I, SOC), prev(I_PREV, I), soc(I_PREV, SOC_PREV), |SOC - SOC_PREV| < 1000, |P_L - P_PV| < 500, vFrom_grid(D, T_PREV, F), time(I_PREV, T_PREV), F = 0.

% Se al tempo target la potenza richiesta è superiore a quella prodotta dal fotovoltaico e lo stato di carica della batteria è sopra la soglia minima consentita, il sistema raccomanda la scarica della batteria.
recommend(D, T, "dicharge") :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, timeTarget(T), time(I, T), socPercentage(I, SOCP), SOCP > EMINP, vE_SminPercentage(EMINP).
% Se al tempo target la potenza prodotta dal fotovoltaico è superiore a quella richiesta e lo stato di carica della batteria è sotto la soglia massima consentita, il sistema raccomanda di caricare la batteria.
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
#show nighttime/2.
#show season/1.

