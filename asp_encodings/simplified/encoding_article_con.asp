date(D) :- vP_L(D, T, P_L).

&dom{-G*2..G*2} = xP_S(D, I) :- date(D), time(I, T), vGUESSMAX(G).

%&sum{P_L; -P_PV; -xP_S(D, I)} = xP_G(D, I) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), time(I, T).
%&sum{xP_G(D, I): time(I, T)} = v :- date(D).
%&minimize{v}.

%&sum{xP_S(D, I): time(I, T)} = d:- date(D).
&minimize {xP_S(D, I): time(I, T), date(D)}.

%&diff { a - d } <= 0 :- d >= 0.
%&diff { a + d } <= 0 :- d < 0.

% Ora a = |d|
%&maximize { a }.


%&minimize{xP_G(D, I) : date(D), time(I, T)}.
%&minimize{xP_S(D, I) : date(D), time(I, T)}.

%&sum{-xP_S(D, I)} <= PL - P_PV :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, K = P_L - P_PV, time(I, T).
&sum{xP_S(D, I)} >= P_PV - P_L :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, time(I, T).
%&sum{-xP_S(D, I)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, time(I, T).

%&sum{xP_S(D, I)} <= K :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, K = P_PV - P_L, time(I, T).
%&sum{xP_S(D, I)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, time(I, T).

%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
%&sum{xE_S(D, 0)} = E_Sinit :- vE_Sinit(E_Sinit), date(D).
%&sum{xE_S(D, 0)} = c :- vE_Sinit(E_Sinit), date(D).
%&sum{xE_S(D,J), J > I} >= xE_S(D, I) :- date(D), time(I, T).
%&sum{xE_S(D,I)} <= E_Smax :- vE_Smax(E_Smax), date(D), time(I, T).
%&sum{xE_S(D,I)} >= E_Smin :- vE_Smin(E_Smin), date(D), time(I, T).

&sum{xP_S(D, J): time(J, _), J <= I} <= E_Smax - E_Sinit :- date(D), time(I, T), vE_Smax(E_Smax), vE_Sinit(E_Sinit).
&sum{xP_S(D, J): time(J, _), J <= I} >= E_Smin - E_Sinit :- date(D), time(I, T), vE_Smin(E_Smin), vE_Sinit(E_Sinit).


%% P_Smin <= PS_t_d <= P_Smax
%&sum{-xP_S(D, I): xP_S(D, I) < 0} <= P_Smax :- date(D), time(I, T), vP_Smax(P_Smax).
%&sum{-xP_S(D, I): xP_S(D, I) < 0} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin).


%&show {xP_S(D, I): date(D), time(I, T)}.
%&show {xP_G(D, I): date(D), time(I, T)}.
%&show {xE_S(D, I): date(D), time(I, T)}.

