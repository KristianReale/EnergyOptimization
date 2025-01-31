vGUESS(0..999).
%%%%  GUESS VARIABILI DI DECISIONE
{vS_P_i_j(D, I, J, S_P_i_j): vGUESS(S_P_i_j)} = 1 :- time(I), date(D), user(J).
{vS_M_i_j(D, I, J, S_M_i_j): vGUESS(S_M_i_j)} = 1 :- time(I), date(D), user(J).
{vC_P_i_j(D, I, J, C_P_i_j): vGUESS(C_P_i_j)} = 1 :- time(I), date(D), user(J).
{vC_M_i_j(D, I, J, C_M_i_j): vGUESS(C_M_i_j)} = 1 :- time(I), date(D), user(J). 


%%%% FUNZIONE OBIETTIVO
:~ vS_P_i_j(D, I, J, S_P_i_j). [S_P_i_j@1, I, J]
:~ vS_M_i_j(D, I, J, S_M_i_j). [S_M_i_j@1, I, J]
:~ vC_P_i_j(D, I, J, C_P_i_j). [C_P_i_j@1, I, J]
:~ vC_M_i_j(D, I, J, C_M_i_j). [C_M_i_j@1, I, J]


%%%% VINCOLI
%:- #sum{S_P_i_j, J, 1: vS_P_i_j(D, I, J, S_P_i_j); -S_M_i_j, J, 2: vS_M_i_j(D, I, J, S_M_i_j)} != CHARGING_i, vCHARGING_i(D, I, CHARGING_i).

:- #sum{C_M_i_j, 1: vC_M_i_j(D, I, J, C_M_i_j); Q_i_j, 2: vQ_i_j(D, I, J, Q_i_j); -P_i_j, 3: vP_i_j(D, I, J, P_i_j); S_P_i_j, 4: vS_P_i_j(D, I, J, S_P_i_j); -S_M_i_j, 5: vS_M_i_j(D, I, J, S_M_i_j)} != C_P_i_j, vC_P_i_j(D, I, J, C_P_i_j).

:- C_P_i_j > Q_i_j + S_P_i_j, vC_P_i_j(D, I, J, C_P_i_j), vS_P_i_j(D, I, J, S_P_i_j), vQ_i_j(D, I, J, Q_i_j).

:- C_M_i_j > P_i_j + S_M_i_j, vC_M_i_j(D, I, J, C_M_i_j), vS_M_i_j(D, I, J, S_M_i_j), vP_i_j(D, I, J, P_i_j).

:- #sum{S_P_i_j, I, 1: vS_P_i_j(D, I, J, S_P_i_j); -S_M_i_j, I, 2: vS_M_i_j(D, I, J, S_M_i_j)} > EMax_j, vEMax_j(D, J, EMax_j).


%vRE_j("2019-12-03", I + 1, J, RE_j + S_P_i_j - S_M_i_j) :- vRE_j("2019-12-03", I, J, RE_j), vS_P_i_j(D, I, J, S_P_i_j), vS_M_i_j(D, I, J, S_M_i_j).

:- #sum{S_P_i_j, I, 1: vS_P_i_j(D, I, J, S_P_i_j); -S_M_i_j, I, 2: vS_M_i_j(D, I, J, S_M_i_j)} > CapTot_j - RE_j, user(J), vCapTot_j(D, J, CapTot_j), vRE_j(D, 0, J, RE_j).


#show vRE_j/4.
#show vS_P_i_j/4.  
#show vS_M_i_j/4.

#show time/1.
#show date/1.


