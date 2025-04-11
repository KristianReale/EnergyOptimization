vGUESS(0..99).

%time(0..2). date("2020-01-01").
date(D) :- vP_L(D, I, P_L).
%time(I) :- vP_L(D, I, P_L).

%%%%  GUESS VARIABILI DI DECISIONE
% INPUT
%{vP_L(D, I, P_L): vGUESS(P_L)} = 1 :- time(I), date(D).
%{vP_PV(D, I, P_PV): vGUESS(P_PV)} = 1 :- time(I), date(D).

% {vP_S(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
% {vCharge(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
%%{vDischarge(D, I, P_S * 10): vGUESS(P_S * 10), vP_Smin(P_Smin), vP_Smax(P_Smax), P_S * 10 >= P_Smin, P_S * 10 <= P_Smax} = 1 :- time(I), date(D).
{vDischarge(D, T, P_S * 10): vGUESS(P_S)} = 1 :- time(I, T), date(D).



%%%% FUNZIONE OBIETTIVO
%:~ F = P_L - P_PV - P_S, vP_L(D, I, P_L), vP_PV(D, I, P_PV), vP_S(D, I, P_S).  [F@1, I]
%:~ vP_L(D, I, P_L).  [P_L@1, I]
%:~ vP_PV(D, I, P_PV).  [-P_PV@1, I]

% :~ vP_S(D, I, P_S).  [-P_S@1, I]
%:~ vCharge(D, I, P_S).  [-P_S@1, I]
:~ vDischarge(D, I, DIS).  [-DIS@1, D, I]

% Charge only the quantity needed of energy taken from the starage is bigger than the consumption
vP_G(D, I, P_L - P_PV - M - DIS) :- vDischarge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV), buyMore(D, I, M).
:~ vP_G(D, I, C), C < 0. [1@2, D, I]
%%:- vFrom_grid(D, I, G), vDischarge(D, I, DIS), G > 0, DIS > 0.



% Sells or charges energy in excess
{vFeed_in(D, I, F * 10): vGUESS(F), F * 10 <= -C} = 1 :-  vP_G(D, I, C), C < 0.
vCharge(D, I, RES) :- vP_G(D, I, C), C < 0, vFeed_in(D, I, F), RES = -C - F.
vFeed_in(D, I, 0) :- vP_G(D, I, C), C >= 0.
vCharge(D, I, 0) :- vP_G(D, I, C), C >= 0.
:- vCharge(D, I, CH), vDischarge(D, I, DIS), CH > 0, DIS > 0.


% If buy from grid
existsBuyMore(D, T) :- buyMore(D, T, M), M > 0.
buyMore(D, T, 0) :- not existsBuyMore(D, I), date(D), time(I, T).
vFrom_grid(D, I, M) :- vP_G(D, I, C), buyMore(D, I, M), C < 0.
vFrom_grid(D, I, M + C) :- vP_G(D, I, C), buyMore(D, I, M), C >= 0.


%%%% VINCOLI
%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
:- time(I, T1), vE_Smin(E_Smin), E_Smin - E_Sinit > #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).
:- time(I, T1), vE_Smax(E_Smax), #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2),J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I} > E_Smax - E_Sinit, vE_Sinit(E_Sinit).


%% P_Smin <= PS_t_d <= P_Smax
:- P_Smin > P_S, vDischarge(D, I, P_S), vP_Smin(P_Smin).
:- P_S > P_Smax, vDischarge(D, I, P_S), vP_Smax(P_Smax).

#show vP_L/3.
#show vP_PV/3.
#show vP_G/3.
#show vCharge/3.
#show vDischarge/3.
#show vFeed_in/3.
#show vFrom_grid/3.
#show vE_Sinit/1.

%UNICAL
%minimo 5%
%unical max 16kw cubo 18B
%unical max 32kw cubo 41B

