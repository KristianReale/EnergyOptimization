vGUESS(0..999).

time(1..23). date("2020-01-01").

%%%%  GUESS VARIABILI DI DECISIONE
% INPUT
%{vP_L(D, I, P_L): vGUESS(P_L)} = 1 :- time(I), date(D).
%{vP_PV(D, I, P_PV): vGUESS(P_PV)} = 1 :- time(I), date(D).

% OUTPUT
% {vP_S(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
% {charge(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
{discharge(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
%date(D) :- vP_L(D, I, P_L).
%time(I) :- vP_L(D, I, P_L).

%%%% FUNZIONE OBIETTIVO
%:~ F = P_L - P_PV - P_S, vP_L(D, I, P_L), vP_PV(D, I, P_PV), vP_S(D, I, P_S).  [F@1, I]
%:~ vP_L(D, I, P_L).  [P_L@1, I]
%:~ vP_PV(D, I, P_PV).  [-P_PV@1, I]

% :~ vP_S(D, I, P_S).  [-P_S@1, I]
% :~ charge(D, I, P_S).  [P_S@1, I]
:~ discharge(D, I, P_S).  [-P_S@1, I]
%:- #sum{P_S1, 1: discharge(D, I, P_S1); -P_S2, 2: charge(D, I, P_S2)}.


%%%% VINCOLI
% Discharge only residual energy
:- discharge(D, I, DIS), DIS > #sum{-P_S1, 1: discharge(D, J, P_S1), J < I; P_S2, 2: charge(D, J, P_S2), J < I; E_Sinit, 3: vE_Sinit(E_Sinit)}, date(D).

% Charge only the quantity needed of energy taken from the starage is bigger than the consumption
% P_S(D, I, P_L - P_PV - DIS) :- discharge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV), DIS < P_L - P_PV, P_L > P_PV.

vP_S(D, I, P_L - P_PV - DIS) :- discharge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV).%, DIS < P_L - P_PV.
charge(D, I, -C) :- vP_S(D, I, C), C < 0.

%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
%:- E_Smin - E_Sinit  > #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I}, date(D), vE_Sinit(E_Sinit), vE_Smin(E_Smin).
%:- #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I} > E_Smax - E_Sinit, date(D), vE_Sinit(E_Sinit), vE_Smax(E_Smax).


%% P_Smin <= PS_t_d <= P_Smax
%:- P_Smin > P_S, vP_S(D, I, P_S), vP_Smin(P_Smin).
%:- P_S > P_Smax, vP_S(D, I, P_S), vP_Smax(P_Smax).

#show vP_L/3.
#show vP_PV/3.
#show vP_S/3.
#show charge/3.
#show discharge/3.

