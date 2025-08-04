
date(D) :- vP_L(D, I, P_L).


%%%%  GUESS VARIABILI DI DECISIONE
{vDischarge(D, T, P_S ): vGUESS(P_S)} = 1 :- time(I, T), date(D), T = "23:59".

:~ vDischarge(D, I, DIS).  [-DIS@2, D, I]

% Charge only the quantity needed of energy taken from the starage is bigger than the consumption
vP_G(D, I, P_L - P_PV - DIS) :- vDischarge(D, I, DIS), vP_L(D, I, P_L), vP_PV(D, I, P_PV).
:- vP_PV(D, I, P_PV), vP_L(D, I, P_L), P_PV >= P_L, vDischarge(D, I, DIS), DIS > 0.

{vCharge(D, I, F ): vGUESS(F), F  <= -C} = 1 :-  vP_G(D, I, C), C < 0.
vFeed_in(D, I, RES) :- vP_G(D, I, C), C < 0, vCharge(D, I, F), RES = -C - F.

vFeed_in(D, I, 0) :- vP_G(D, I, C), C >= 0.
vCharge(D, I, 0) :- vP_G(D, I, C), C >= 0.
:- vCharge(D, I, CH), vDischarge(D, I, DIS), CH > 0, DIS > 0.

vFrom_grid(D, I, 0) :- vP_G(D, I, C), C < 0.
vFrom_grid(D, I, C) :- vP_G(D, I, C), C >= 0.

%%%% VINCOLI
%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
:- time(I, T1), T="23:59", vE_Smin(E_Smin), E_Smin - E_Sinit > #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2), J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I}, vE_Sinit(E_Sinit).
%%%%:- time(I, T1), vE_Smax(E_Smax), #sum{-P_S1, J, 1: vDischarge(D, T2, P_S1), time(J, T2),J <= I; P_S2, J, 2: vCharge(D, T2, P_S2), time(J, T2), J <= I} > E_Smax - E_Sinit, vE_Sinit(E_Sinit).

%% P_Smin <= PS_t_d <= P_Smax
:- P_Smin > P_S, vDischarge(D, I, P_S), vP_Smin(P_Smin).
:- P_Smin > P_S, vCharge(D, I, P_S), vP_SminC(P_Smin).


:- vDischarge(D, I, P_S), vP_L(D, I, P_L), vP_PV(D, I, P_PV), P_L > P_PV, P_S > P_L - P_PV.
:~ vCharge(D, I, P_SC), vP_L(D, I, P_L), vP_PV(D, I, P_PV), P_PV > P_L, P_SC < P_PV - P_L. [1@1, D, I]


#show vP_L/3.
#show vP_PV/3.
#show vP_G/3.
#show vCharge/3.
#show vDischarge/3.
#show vFeed_in/3.
#show vFrom_grid/3.
#show vE_Sinit/1.
#show time/2.

%UNICAL
%minimo 5%
%unical max 16kw cubo 18B
%unical max 32kw cubo 41B

