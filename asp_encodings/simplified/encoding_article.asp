vGUESS(0..99).

%time(0..2). date("2020-01-01").
date(D) :- vP_L(D, I, P_L).
time(I) :- vP_L(D, I, P_L).

%%%%  GUESS VARIABILI DI DECISIONE
% INPUT
%{vP_L(D, I, P_L): vGUESS(P_L)} = 1 :- time(I), date(D).
%{vP_PV(D, I, P_PV): vGUESS(P_PV)} = 1 :- time(I), date(D).

% OUTPUT
% {vP_S(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
% {vCharge(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
{vDischarge(D, I, P_S * 1000): vGUESS(P_S)} = 1 :- time(I), date(D).

%vDischarge(D, 0, X) :- vE_Sinit(X), date(D).
%{vDischarge(D, I, 25000)} = 1 :-  time(I), date(D), 25000 - E_Sinit <= #sum{-P_S1, 1: vDischarge(D, J, P_S1), J < I; P_S2, 2: vCharge(D, J, P_S2), J < I}, vE_Sinit(E_Sinit).
%vDischarge(D, I, X) :- time(I), date(D), X = #sum{P_S1, J: vDischarge(D, J, P_S1), J < I}, vE_Sinit(E_Sinit), vDischarge(D, J, P_S1).



%%%% FUNZIONE OBIETTIVO
%:~ F = P_L - P_PV - P_S, vP_L(D, I, P_L), vP_PV(D, I, P_PV), vP_S(D, I, P_S).  [F@1, I]
%:~ vP_L(D, I, P_L).  [P_L@1, I]
%:~ vP_PV(D, I, P_PV).  [-P_PV@1, I]

% :~ vP_S(D, I, P_S).  [-P_S@1, I]
%:~ vCharge(D, I, P_S).  [-P_S@1, I]
:~ vDischarge(D, I, P_S).  [-P_S@1, I]



%%%% VINCOLI
% vDischarge only residual energy
:- vDischarge(D, I, DIS), DIS - E_Sinit > #sum{-P_S1, J, 1: vDischarge(D, J, P_S1), J < I; P_S2, J, 2: vCharge(D, J, P_S2), J < I}, vE_Sinit(E_Sinit), date(D).

% Charge only the quantity needed of energy taken from the starage is bigger than the consumption
vP_G(D, I, P_L - P_PV - DIS) :- vDischarge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV). %, DIS < P_L - P_PV.

% Sells or charges
% vFeed_in(D, I, -C) | vCharge(D, I, -C) :- vP_G(D, I, C), C < 0.

{vFeed_in(D, I, F*1000): vP_G(D, I, C), C < 0, vGUESS(F), F * 1000 <= -C  } = 1. % :- vP_G(D, I, C), C < 0, vGUESS(F), F * 1000 <= -C.
vFeed_in(D, I, 0) :- vP_G(D, I, C), C >= 0.
vCharge(D, I, RES) :- vP_G(D, I, C), C < 0, vFeed_in(D, I, F), RES = -C - F, vP_G(D, I, C), C >= 0.%, not existsCharge(D, I).

%{vCharge(D, I, F*1000) } <= 1 :- vP_G(D, I, C), C < 0, vGUESS(F), F * 1000 <= -C.
%:- vFeed_in(D, I, C1), vCharge(D, I, C2), vP_G(D, I, C), C < 0, C1 + C2 != -C.
%vFeed_in(D, I, RES) :- not existsFeedin(D, I), RES = DIS - P_L + P_PV, RES > 0, vDischarge(D, I, DIS),  vP_L(D, I, P_L), vP_PV(D, I, P_PV).
% :~  vCharge(D, I, C), vDischarge(D, I, DIS),  vP_L(D, I, P_L), vP_PV(D, I, P_PV), vFeed_in(D, I, F), C >= DIS - P_L + P_PV - F. [1]
%:~  vCharge(D, I, C). [-C@2, D, I]
:~  vFeed_in(D, I, C). [-C@2, D, I]


% vFeed_in(D, I, -C) :- vP_G(D, I, C), C < 0.
% :- vCharge(D, I, C), vCharge(D, I, D), C != D.

vFrom_grid(D, I, C) :- vP_G(D, I, C), C > 0.

existsCharge(D, I) :- vCharge(D, I, C), C != 0.
vCharge(D, I, 0) :- not existsCharge(D, I), date(D), time(I).
existsFeedin(D, I) :- vFeed_in(D, I, C), C != 0.
%vFeed_in(D, I, 0) :- not existsFeedin(D, I), date(D), time(I).
existsFrom_grid(D, I) :- vFrom_grid(D, I, C), C != 0.
vFrom_grid(D, I, 0) :- not existsFrom_grid(D, I), date(D), time(I).


%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
%:- E_Smin - E_Sinit  > #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I}, date(D), vE_Sinit(E_Sinit), vE_Smin(E_Smin).
%:- #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I} > E_Smax - E_Sinit, date(D), vE_Sinit(E_Sinit), vE_Smax(E_Smax).


%% P_Smin <= PS_t_d <= P_Smax
%:- P_Smin > P_S, vP_S(D, I, P_S), vP_Smin(P_Smin).
%:- P_S > P_Smax, vP_S(D, I, P_S), vP_Smax(P_Smax).

#show vP_L/3.
#show vP_PV/3.
#show vP_G/3.
#show vCharge/3.
#show vDischarge/3.
#show vFeed_in/3.
#show vFrom_grid/3.
#show vE_Sinit/1.


