date(D) :- vP_L(D, T, P_L).


&dom{-G*2..G*2} = xP_S(D, I, T) :- date(D), time(I, T), vGUESSMAX(G).
%&dom{-G*2..G*2} = xP_S1(D, I, T) :- date(D), time(I, T), vGUESSMAX(G).


%&sum{P_L; -P_PV; -xP_S(D, I, T)} = xP_G(D, I) :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), time(I, T).
%&sum{xP_G(D, I): time(I, T)} = v :- date(D).
%&minimize{v}.

&minimize {xP_S(D, I, T) : time(I, T), diffPV_L(D, T, V, negative)}.
&maximize {xP_S(D, I, T) : time(I, T), date(D), diffPV_L(D, T, V, positive)}.

%&sum{k(D,I)} <= 1 :- date(D), time(I, T).
%&sum{xP_S(D, I, T): k(D,I) = 1} < 0 :- date(D), time(I, T).
%a(1) :- &sum{xP_S(D, I, T)} < 0, time(I, T), diffPV_L(D, T, V, negative).

%&minimize {xP_S(D, I, T) : time(I, T), use(D, T, V)}.






%use("2023-08-26", 1).
%use("2023-08-26", 4).
%use("2023-08-26", 5).

%useMax("2023-12-22", "2:00:00", 5).
%useMax("2023-12-22", "22:00:00", 5).
%useMax("2023-12-22", "18:00:00", 5).
%&sum{xP_S(D, I, T)} >= -V :- useMax(D, T, V), time(I, T).
%&sum{xP_S(D, I, T)} >= -2 :- date(D), time(I, T).

%prefUse(D, T) :- diffPV_L_int(D, T, V, negative), V < -5.
%&minimize{xP_S(D, I, T)} :- prefUse(D, T), time(I, T).



%%use("2023-08-26","1:00:00") use("2023-08-26","3:00:00") use("2023-08-26","5:00:00") use("2023-08-26","6:00:00") use("2023-08-26","7:00:00")
%%use("2023-08-26","8:00:00") use("2023-08-26","19:00:00") use("2023-08-26","20:00:00") use("2023-08-26","21:00:00")

#minimize {1@2, D,T : use(D, T) }.
{use(D, T)} :- diffPV_L_int(D, T, V, negative).
%:- #count{T, D: use(D, T)} > 9.
&sum{xP_S(D, I, T)} < 0 :- use(D, T), time(I, T).
&sum{xP_S(D, I, T)} >= 0 :- not use(D, T), time(I, T), date(D).

%disOpt("119.999"). chOpt("79.999").

%&sum{xP_S(D, I, T): time(I, T), diffPV_L(D, T, V, negative) } <= -DIS_OPT :- disOpt(DIS_OPT).
%&sum{xP_S(D, I, T): time(I, T), diffPV_L(D, T, V, positive)} >= CH_OPT :- chOpt(CH_OPT).

%%%%&dom{0..1} = use(D, T) :- diffPV_L_int(D, T, V, negative).
%%%%&sum{use(D, T)} <= 1 :- date(D), time(I, T).
%%%%&sum{use(D, T): date(D), time(I, T)} = 9.
%%%%aa.
%%%%aa :- &sum{use(D, T)} = 1, date(D), time(I, T).

%&sum { xP_S(D,I,T) } <= 100000 * (1 - use(D,T)) :- date(D), time(I, T).
%&sum { xP_S(D,I,T) } >= use(D,T) - 1 :- date(D), time(I,T).


%%%%a("1000.0").

% se use=1 ⇒ xP_S ≤ 0
%%%%&sum { xP_S(D,I,T) } < M * (1 - use(D,T)) :- date(D), time(I,T), a(M).
%%%%&sum { xP_S(D,I,T)} >= -M * use(D,T) :- date(D), time(I,T), a(M).



%&sum{xP_S(D, I, T)} >= 0 :- not use(D, T), time(I, T), date(D).



%&sum{xP_S1(D, I, T) - xP_S(D, I, T): time(I, T), diffPV_L(D, T, V, negative) } = 0.
%&sum{xP_S1(D, I, T) - xP_S(D, I, T): time(I, T), diffPV_L(D, T, V, positive) } = 0.


%:~ V1 = #sum{V, D, T: use(D, T, V)}. [V1@1]
%#minimize {1@2,D,T: use(D, T) }.

%use(D, T) :- diffPV_L_int(D, T, V, negative), V < -10.
%&sum{xP_S(D, I, T)} >= 0 :- not use(D, T), time(I, T), date(D).



%&sum{xP_S(D, I, T)} <= P_PV - P_L :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV >= P_L, time(I, T).

&sum{xP_S(D, I, T)} <= V :- diffPV_L(D, T, V, positive), time(I, T).
&sum{xP_S(D, I, T)} >= 0 :- diffPV_L(D, T, V, positive), time(I, T).
&sum{xP_S(D, I, T)} >= V :- diffPV_L(D, T, V, negative), time(I, T).
&sum{xP_S(D, I, T)} <= 0 :- diffPV_L(D, T, V, negative), time(I, T).

%&sum{xP_S1(D, I, T)} <= V :- diffPV_L(D, T, V, positive), time(I, T).
%&sum{xP_S1(D, I, T)} >= 0 :- diffPV_L(D, T, V, positive), time(I, T).
%&sum{xP_S1(D, I, T)} >= V :- diffPV_L(D, T, V, negative), time(I, T).
%&sum{xP_S1(D, I, T)} <= 0 :- diffPV_L(D, T, V, negative), time(I, T).

%&sum{-xP_S(D, I, T): xP_S(D, I, T) < 0} >= P_L - P_PV :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, time(I, T).

%&sum{-xP_S(D, I, T)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_L > P_PV, time(I, T).

%&sum{xP_S(D, I, T)} <= K :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, K = P_PV - P_L, time(I, T).
%&sum{xP_S(D, I, T)} >= 0 :- vP_L(D, T, P_L), vP_PV(D, T, P_PV), P_PV > P_L, time(I, T).

%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
%&sum{xE_S(D, 0)} = E_Sinit :- vE_Sinit(E_Sinit), date(D).
%&sum{xE_S(D, 0)} = c :- vE_Sinit(E_Sinit), date(D).
%&sum{xE_S(D,J), J > I} >= xE_S(D, I) :- date(D), time(I, T).
%&sum{xE_S(D,I)} <= E_Smax :- vE_Smax(E_Smax), date(D), time(I, T).
%&sum{xE_S(D,I)} >= E_Smin :- vE_Smin(E_Smin), date(D), time(I, T).

&sum{xP_S(D, J, T1): time(J, T1), J <= I} <= E_Smax - E_Sinit :- date(D), time(I, T), vE_Smax(E_Smax), vE_Sinit(E_Sinit).
&sum{xP_S(D, J, T1): time(J, T1), J <= I} >= E_Smin - E_Sinit :- date(D), time(I, T), vE_Smin(E_Smin), vE_Sinit(E_Sinit).



%nonzero(D,J) :-
%    date(D), time(J,T),
%    &sum { xP_S(D,J,T) } < 0.
%&maximize{xP_S(D, J, T1) - xP_S(D, J2, T2)} :- date(D), time(J, T1), time(J2, T2), J = J2 + 1, J2 > 1.


%&sum {k(D, I) * xP_S(D,I,T)} < 0 :- diffPV_L(D, T, V, negative), time(I,T).
%a(D, T) :- &sum { xP_S(D,I,T) } < 0, date(D), time(I,T).

%&sum { k(D, I) } = 2 :- diffPV_L(D, T, V, negative), time(I, T).
%&sum { k(D, I) } = 0 :- diffPV_L(D, T, V, positive), time(I, T).
%&sum { k(D, I) * xP_S(D,I,T) } < 0 :- date(D), time(I,T).
%&minimize { k(D,I) * xP_S(D,I,T) : date(D), time(I,_) }.


%% P_Smin <= PS_t_d <= P_Smax
%&sum{-xP_S(D, I): xP_S(D, I) < 0} <= P_Smax :- date(D), time(I, T), vP_Smax(P_Smax).
%&sum{-xP_S(D, I): xP_S(D, I) < 0} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin).
%%&sum{xP_S(D, I, T)} >= -P_Smax :- date(D), time(I, T), vP_Smax(P_Smax), diffPV_L(D, T, V, negative).
%%&sum{xP_S(D, I, T)} <= P_Smax :- date(D), time(I, T), vP_Smax(P_Smax), diffPV_L(D, T, V, positive).
%%&sum{-xP_S(D, I, T)} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin), diffPV_L(D, T, V, negative).
%%&sum{xP_S(D, I, T)} >= P_Smin :- date(D), time(I, T), vP_Smin(P_Smin), diffPV_L(D, T, V, positive).


%&show {xP_S(D, I): date(D), time(I, T)}.
%&show {xP_G(D, I): date(D), time(I, T)}.
%&show {xE_S(D, I): date(D), time(I, T)}.


