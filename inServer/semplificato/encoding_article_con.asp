date(D) :- vP_L(D, I, P_L).

%%%%  GUESS VARIABILI DI DECISIONE
%{vDischarge(D, T, P_S): vGUESS(P_S)} = 1 :- time(I, T), date(D).
%vDischarge(D, T, 0) :- time(I, T), date(D), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L < P_PV.
%:~ vDischarge(D, I, DIS).  [-DIS@2, D, I]

&dom{0..G} = xDischarge(D, T) :-  vGUESSMAX(G), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV >= P_L, G1 = P_PV - P_L.
&maximize {xDischarge(D, T) : time(I, T), date(D)}.


% Charge only the quantity needed of energy taken from the starage is bigger than the consumption
%vP_G(D, I, P_L - P_PV - DIS) :- vDischarge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV).
%&sum{P_L - P_PV - DIS} < 10 :- DIS = xDischarge(D, T), vP_L(D, T, P_L), vP_PV(D, T, P_PV).

%:- vP_PV(D, I, P_PV), vP_L(D, I, P_L), P_PV >= P_L, vDischarge(D, I, DIS), DIS > 0.
&sum{xDischarge(D, I)} = 0 :- vP_PV(D, I, P_PV), vP_L(D, I, P_L), P_PV >= P_L.


% Sells or charges energy in excess
%{vCharge(D, I, F ): vGUESS(F), F  <= -C} = 1 :-  vP_G(D, I, C), C < 0.
%&dom{0..G1} = xCharge(D, T) :-  vGUESSMAX(G), vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L >= P_PV, G1 = P_L - P_PV.
&dom{0..G} = xCharge(D, T) :-  vGUESSMAX(G), date(D), time(I, T).
%&maximize {xCharge(D, T) : time(I, T), date(D)}.


%vFeed_in(D, I, RES) :- vP_G(D, I, C), C < 0, F = Charge(D, I, F), RES = -C - F.

%&dom{0..G} = xFeed_in(D, T) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV >= P_L, G1 = P_PV - P_L.
&dom{0..G} = xFeed_in(D, T) :- vGUESSMAX(G), date(D), time(I, T).
&sum{xFeed_in(D, T)} = 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV < P_L.
&sum{xFeed_in(D, T)} <= G1 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV >= P_L, G1 = P_PV - P_L.

&dom{0..G} = xFrom_grid(D, T) :- vGUESSMAX(G), date(D), time(I, T).
&sum{xFrom_grid(D, T)} = 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L.
&sum{xFrom_grid(D, T)} <= G1 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV <= P_L, G1 = P_L - P_PV.

%&sum{xFrom_grid(D, T); xDicharge(D, T)} = G1 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L >= P_PV, G1 = P_L - P_PV.

%{xDicharge(D, T)} > 10 :- vP_L(D, T, P_L).






