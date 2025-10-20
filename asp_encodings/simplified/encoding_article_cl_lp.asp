date(D) :- vP_L(D, T, P_L).

&dom{-G*2..G*2} = xP_S(D, I, T) :- date(D), time(I, T), vGUESSMAX(G).

&minimize {xP_S(D, I, T): time(I, T), date(D)} :- diffPV_L(D, T, V, negative).
&maximize {xP_S(D, I, T): time(I, T), date(D)} :- diffPV_L(D, T, V, positive).


&sum{xP_S(D, I, T)} <= V :- diffPV_L(D, T, V, positive), time(I, T).
&sum{xP_S(D, I, T)} >= 0 :- diffPV_L(D, T, V, positive), time(I, T).
&sum{xP_S(D, I, T)} >= V :- diffPV_L(D, T, V, negative), time(I, T).
&sum{xP_S(D, I, T)} <= 0 :- diffPV_L(D, T, V, negative), time(I, T).


&sum{xP_S(D, J, T1): time(J, T1), J <= I} <= E_Smax - E_Sinit :- date(D), time(I, T), vE_Smax(E_Smax), vE_Sinit(E_Sinit).
&sum{xP_S(D, J, T1): time(J, T1), J <= I} >= E_Smin - E_Sinit :- date(D), time(I, T), vE_Smin(E_Smin), vE_Sinit(E_Sinit).


%% P_Smin <= PS_t_d <= P_Smax
%&sum{-xP_S(D, I): xP_S(D, I) < 0} <= P_Smax :- date(D), time(I, T), vP_Smax(P_Smax).
%&sum{-xP_S(D, I): xP_S(D, I) < 0} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin).


%&show {xP_S(D, I): date(D), time(I, T)}.
%&show {xP_G(D, I): date(D), time(I, T)}.
%&show {xE_S(D, I): date(D), time(I, T)}.


