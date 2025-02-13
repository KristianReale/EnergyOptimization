vGUESS(0..999).

% time(1..23). date(1).

%%%%  GUESS VARIABILI DI DECISIONE
{vP_L(D, I, P_L): vGUESS(P_L)} = 1 :- time(I), date(D).
{vP_PV(D, I, P_PV): vGUESS(P_PV)} = 1 :- time(I), date(D).

% INPUT
% {vP_S(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).
date(D) :- vP_S(D, I, P_S).
time(I) :- vP_S(D, I, P_S).

%%%% FUNZIONE OBIETTIVO
%:~ F = P_L - P_PV - P_S, vP_L(D, I, P_L), vP_PV(D, I, P_PV), vP_S(D, I, P_S).  [F@1, I]
:~ vP_L(D, I, P_L).  [P_L@1, I]
:~ vP_PV(D, I, P_PV).  [-P_PV@1, I]
% :~ vP_S(D, I, P_S).  [-P_S@1, I]

%%%% VINCOLI
%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
:- E_Smin - E_Sinit  > #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I} > E_Smax - E_Sinit, date(D), vE_Sinit(E_Sinit), vE_Smin(E_Smin), vE_Smax(E_Smax).


%% P_Smin <= PS_t_d <= P_Smax
:- P_Smin > P_S, P_S > P_Smax, vP_S(D, I, P_S), vP_Smin(P_Smin), vP_Smax(P_Smax).

#show vP_L/3.
#show vP_PV/3.
#show vP_S/3.

