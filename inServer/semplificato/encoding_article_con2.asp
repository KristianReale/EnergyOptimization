% Predicate Descriptions
% date(D) represents a date: D is a string representing a date.
% time(I, T) represents a time hour: I is an incremental time index, while T a string representing a time hour in the format %H:%M:%S.
% vGUESSMAX(G), G representes the maximum domain value that can be assigned to xP_S.
% vP_L(D, T, P_L) representes the Energy Load (Consumption) where D is a date and T is a hour in a day
% vP_PV(D, T, P_L) representes the Energy Production where D is a date and T is a hour in a day
% xE_S(D, I) represents the quantity of energy stored to the battery. It is a clingcon function symbol.
% vE_Smin(E_Smin) represents the minimum storage energy level that the battery can have.
% vE_Smax(E_Smax) represents the maximum storage energy level that the battery can have.
% vE_Sinit(E_Sinit) represents the initial storage energy level of the battery.
% xP_S(D, I), decision variable, represents the quantity of power charged/discharged from the battery, at date D and time index I
%       It is a clingcon function symbol where the value ranges between a negative value and a positive value.
%       If the value is positive, it refers to the amount of energy used to charge the battery (charge).
%       If the value is negative, it refers to the quantity of energy taken from the battery (discharge)
% xP_G(D, I), objective function, it represents the quantity of Energy exchanged with the grid, at date D and time index I
%       It is a clingcon function symbol where the value is the result of P_L - P_PV - xP_S(D, I) where
            P_L is the Energy Load value coming from vP_L(D, T, P_L), at date D, time T
            P_PV is the Energy Production coming from vP_PV(D, T, P_L), at date D, time T
            xP_S(D, I) represents the quantity of power charged/discharged from the battery, at date D, time index I
%       If the value is positive, it refers to the energy taken from the grid.
%       If the value is negative, it refers to the energy fed to the grid.

date(D) :- vP_L(D, T, P_L).

&dom{-G*2..G*2} = xP_S(D, I) :- date(D), time(I, T), vGUESSMAX(G).
&sum{P_L; -P_PV; -xP_S(D, I)} = xP_G(D, I) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), time(I, T).
%&sum{xP_G(D, I): time(I, T)} = v :- date(D).
%&minimize{v}.
&sum{xP_S(D, I): time(I, T)} = d :- date(D).
&minimize{d}.
%&minimize{xP_G(D, I) : date(D), time(I, T)}.
%&minimize{xP_S(D, I) : date(D), time(I, T)}.

&sum{-xP_S(D, I)} <= K :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, K = P_L - P_PV, time(I, T).
&sum{-xP_S(D, I)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, K = P_L - P_PV, time(I, T).

&sum{xP_S(D, I)} <= K :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, K = P_PV - P_L, time(I, T).
&sum{xP_S(D, I)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, K = P_PV - P_L, time(I, T).

%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
&sum{xE_S(D, 0)} = E_Sinit :- vE_Sinit(E_Sinit), date(D).
&sum{xE_S(D, I - 1); xP_S(D, I)} = xE_S(D, I) :- date(D), time(I, T), I > 0.
&sum{xE_S(D, I)} <= E_Smax :- vE_Sinit(E_Sinit), vE_Smax(E_Smax), date(D), time(I, T).
&sum{xE_S(D, I)} >= E_Smin :- vE_Smin(E_Smin), date(D), time(I, T).


%% P_Smin <= PS_t_d <= P_Smax
%&sum{-xP_S(D, I): xP_S(D, I) < 0} <= P_Smax :- date(D), time(I, T), vP_Smax(P_Smax).
%&sum{-xP_S(D, I): xP_S(D, I) < 0} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin).


&show {xP_S(D, I): date(D), time(I, T)}.
&show {xP_G(D, I): date(D), time(I, T)}.
&show {xE_S(D, I): date(D), time(I, T)}.

