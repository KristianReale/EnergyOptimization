vGUESS(0..999).
 
%%%%  GUESS VARIABILI DI DECISIONE
{vC_P(D, I, C_IP): vGUESS(C_IP), vQ(D, I, Q_I), C_IP <= Q_I, vCREG_MINUS(D, I, CREG_IM), CREG_IM <= C_IP} = 1 :- time(I), date(D).
{vC_M(D, I, C_IM): vGUESS(C_IM), vP(D, I, P_I), C_IM <= P_I} = 1 :- time(I), date(D). 
{vE_P1(D, I, E_IP1): vGUESS(E_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= E_IP1} = 1 :- time(I), date(D). 
{vE_M1(D, I, E_IM1): vGUESS(E_IM1)} = 1 :- time(I), date(D).
{vS_P1(D, I, S_IP1): vGUESS(S_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= S_IP1} = 1 :- time(I), date(D).
{vS_M1(D, I, S_IM1): vGUESS(S_IM1)} = 1 :- time(I), date(D).


%%%% FUNZIONE OBIETTIVO
%:~ K = A + B - C + D - E - F,
%				A = PUN_I * C_IP - PZ_I * C_IM, 
%					vPUN(D, I, PUN_I), vC_P(D, I, C_IP), 
%					vC_M(D, I, C_IM), vPZ(D, I, PZ_I),
%				B = CostCharge1 * S_IP1 + CostDischarge1 * S_IM1,
%					vCostCharge1(CostCharge1), vS_P1(D, I, S_IP1), 
%					vCostDischarge1(CostDischarge1), vS_M1(D, I, S_IM1), 
%				C = PAP + E_IP1,
%					vPAP(PAP), vE_P1(D, I, E_IP1),
%				D = PVP + E_IM1,
%					vPVP(PVP), vE_M1(D, I, E_IM1),
%				E = POFF_IP * CREG_IP,
%					vPOFF_PLUS(D, I, POFF_IP), vCREG_PLUS(D, I, CREG_IP),
%				F = POFF_IM * CREG_IM,
%					vPOFF_MINUS(D, I, POFF_IM), vCREG_MINUS(D, I, CREG_IM).
%   [K]

% :~ A = PUN_I * C_IP - PZ_I * C_IM,  vPUN(D, I, PUN_I), vC_P(D, I, C_IP),  vC_M(D, I, C_IM), vPZ(D, I, PZ_I). [A@1, I]   
:~ A = PUN_I * C_IP,  vPUN(D, I, PUN_I), vC_P(D, I, C_IP). [A@1, I]
:~ A = (PZ_I * C_IM) / 1000,  vC_M(D, I, C_IM), vPZ(D, I, PZ_I). [-A@1, I]
% :~ B = CostCharge1 * S_IP1 + CostDischarge1 * S_IM1, vCostCharge1(CostCharge1), vS_P1(D, I, S_IP1),  vCostDischarge1(CostDischarge1), vS_M1(D, I, S_IM1). [B@1, I]
:~ B = CostCharge1 * S_IP1, vCostCharge1(CostCharge1), vS_P1(D, I, S_IP1). [B@1, I]
:~ B = CostDischarge1 * S_IM1, vCostDischarge1(CostDischarge1), vS_M1(D, I, S_IM1). [B@1, I]
:~ C = PAP + E_IP1, vPAP(PAP), vE_P1(D, I, E_IP1). [-C@1, I]
:~ D = PVP + E_IM1, vPVP(PVP), vE_M1(D, I, E_IM1), E = POFF_IP * CREG_IP, vPOFF_PLUS(D, I, POFF_IP), vCREG_PLUS(D, I, CREG_IP), F = POFF_IM * CREG_IM, vPOFF_MINUS(D, I, POFF_IM), vCREG_MINUS(D, I, CREG_IM). [D-E-F@1, I]


%%%% VINCOLI

%% C_IP - C_IM = (Q_I - P_I) + S_I1 + E_I1 - CREG_IM + CREG_IP
:- #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2: vS_M1(D, I, S_IM1); E_IP1,3: vE_P1(D, I, E_IP1); -E_IM1,4: vE_M1(D, I, E_IM1); -C_IP,5: vC_P(D, I, C_IP); C_IM,6: vC_M(D, I, C_IM)} != P_I - Q_I + CREG_IM - CREG_IP, vCREG_MINUS(D, I, CREG_IM), vCREG_PLUS(D, I, CREG_IP), vQ(D, I, Q_I), vP(D, I, P_I).
%:- #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2: vS_M1(D, I, S_IM1); E_IP1,3: vE_P1(D, I, E_IP1); -E_IM1,4: vE_M1(D, I, E_IM1); -C_IP,5: vC_P(D, I, C_IP); 
%			C_IM,6: vC_M(D, I, C_IM); -CREG_IM, 7: vCREG_MINUS(D, I, CREG_IM); CREG_IP, 8: vCREG_PLUS(D, I, CREG_IP)} 
%	!= P_I - Q_I, vQ(D, I, Q_I), vP(D, I, P_I).
% :- C_IP - C_IM != (Q_I - P_I) + S_I1 + E_I1 - CREG_IM + CREG_IP, S_I1 = S_IP1 - S_IM1, E_I1 = E_IP1 - E_IM1, vC_P(D, I, C_IP), vC_M(D, I, C_IM), vQ(D, I, Q_I), vP(D, I, P_I), vCREG_MINUS(D, I, CREG_IM), vCREG_PLUS(D, I, CREG_IP), vS_P1(D, I, S_IP1), vS_M1(D, I, S_IM1),  vE_P1(D, I, E_IP1), vE_M1(D, I, E_IM1).

%% CREG_IM <= S_IP1 + E_IP1 + C_IP
%:- CREG_IM != 0, CREG_IM > S_IP1 + E_IP1 + C_IP, vCREG_MINUS(D, I, CREG_IM), vS_P1(D, I, S_IP1), vE_P1(D, I, E_IP1), vC_P(D, I, C_IP).
:- CREG_IM != 0, CREG_IM > 
	#sum{S_IP1, 1: vS_P1(D, I, S_IP1); E_IP1,2: vE_P1(D, I, E_IP1); C_IP,3: vC_P(D, I, C_IP)}, vCREG_MINUS(D, I, CREG_IM).

%% E_IP1 <= OVER_I * Percentage_Ps1
%mult1(X) :- X = OVER_I * Percentage_Ps1, vOVER_I(D, I, OVER_I), vPercentage_Ps1(Percentage_Ps1).
%mult11(X) :- mult1(X), X <= 999.
%mult11(Y) :- mult1(X), X > 999, Y = X / 1000.
%:- E_IP1 > X, vE_P1(D, I, E_IP1), mult11(X).
%:- E_IP1 * 1000 > (OVER_I * Percentage_Ps1) , vE_P1(D, I, E_IP1), vOVER_I(D, I, OVER_I), vPercentage_Ps1(Percentage_Ps1).
:- E_IP1 * 10 > (OVER_I * Percentage_Ps1) , vE_P1(D, I, E_IP1), vOVER_I(D, I, OVER_I), vPercentage_Ps1(Percentage_Ps1).


%% E_IM1 <= UNDER_I * Percentage_Ms1
%:- E_IM1 * 1000 > (UNDER_I * Percentage_Ms1), vE_M1(D, I, E_IM1), vUNDER_I(D, I, UNDER_I), vPercentage_Ms1(Percentage_Ms1).
:- E_IM1 * 10 > (UNDER_I * Percentage_Ms1), vE_M1(D, I, E_IM1), vUNDER_I(D, I, UNDER_I), vPercentage_Ms1(Percentage_Ms1).


%% EMin1 <= S_IP1 - S_IM1 <= EMax1
 :- EMin1 > #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2:vS_M1(D, I, S_IM1)} > EMax1, vEMin1(EMin1), vEMax1(EMax1).  % :- EMin1 > S_IP1 - S_IM1, vEMin1(EMin1), vS_P1(D, I, S_IP1), vS_M1(D, I, S_IM1).
 % :- #sum{S_IP1,I,1: vS_P1(D, I, S_IP1); -S_IM1,I,2:vS_M1(D, I, S_IM1)} > EMax1, vEMax1(EMax1).  % :- S_IP1 - S_IM1 > EMax1, vEMax1(EMax1), vS_P1(D, i, S_IP1), vS_M1(D, I, S_IM1).

%% CAP_TOT_MIN_1 <= SSOC_I + S_IP1 - S_IM1 <= CAP_TOT_MAX_1
%vSOC(I + 1, SOC_I1) :- vSOC(I, SOC_I), SOC_I1 = SOC_I + S_IP1 - S_IM1, vS_P1(D, I, S_IP1), vS_M1(D, I, S_IM1).
:- vSOC(I, SOC_I), #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2: vS_M1(D, I, S_IM1)} > CAP_TOT_MAX_1 - SOC_I,  vCapTotMax_1(CAP_TOT_MAX_1). 
%%%:- vSOC(I, SOC_I), SOC_I + S_IP1 - S_IM1 > CAP_TOT_MAX_1, vS_P1(D, I, S_IP1), vS_M1(D, I, S_IM1), vCapTotMax_1(CAP_TOT_MAX_1).

%% EMinS1 <= E_IP1 - E_IM1 <= EMaxS1
:- vEMinS1(EMinS1), EMinS1 > #sum{E_IP1,1: vE_P1(D, I, E_IP1); -E_IM1,2: vE_M1(D, I, E_IM1)} > EMaxS1, vEMaxS1(EMaxS1). % :- EMinS1 > E_IP1 - E_IM1, vEMinS1(EMinS1), vE_P1(D, I, E_IP1), vE_M1(D, I, E_IM1).
% :- E_IP1 - E_IM1 > EMaxS1, vEMaxS1(EMaxS1), vE_P1(D, I, E_IP1), vE_M1(D, I, E_IM1).


%% CAP_TOT_MIN_S1 <= SOC_SI + E_IP1 - E_IM1 <= CAP_TOT_MAX_S1
% vSOC_S(I + 1, SOC_SI1) :- vSOC_S(I, SOC_SI), SOC_SI1 = SOC_SI + E_IP1 - E_IM1, vE_P1(D, I, E_IP1), vE_M1(D, I, E_IM1).
:- #sum{E_IP1,1 : vE_P1(D, I, E_IP1); -E_IM1,2: vE_M1(D, I, E_IM1)} > CAP_TOT_MAX_S1 - SOC_SI, vSOC_S(I, SOC_SI), vCapTotMax_S1(CAP_TOT_MAX_S1).
%%%:- vSOC_S(I, SOC_SI), SOC_SI + E_IP1 - E_IM1 > CAP_TOT_MAX_S1, vE_P1(D, I, E_IP1), vE_M1(D, I, E_IM1), vCapTotMax_S1(CAP_TOT_MAX_S1).

%% 0 <= Percentage_Ps1 <= 1 
:- vPercentage_Ps1(Percentage_Ps1), Percentage_Ps1 > 10.

%% 0 <= Percentage_Ms1 <= 1
:- vPercentage_Ms1(Percentage_Ms1), Percentage_Ms1 > 10.



vOVER_I(D, I, OVER_I) :- P_I >= Q_I, OVER_I = P_I - Q_I, 
									vP(D, I, P_I), vQ(D, I, Q_I).
vOVER_I(D, I, 0) :- P_I < Q_I, 
									vP(D, I, P_I), vQ(D, I, Q_I).

vUNDER_I(D, I, UNDER_I) :- P_I <= Q_I, UNDER_I = Q_I - P_I, 
									vP(D, I, P_I), vQ(D, I, Q_I).
vUNDER_I(D, I, 0) :- P_I > Q_I, 
									vP(D, I, P_I), vQ(D, I, Q_I).

#show vSOC/2.



#show vSOC_S/2.

#show vP/3.
#show vQ/3.
#show vOVER_I/3.
#show vUNDER_I/3.


#show vPUN/3.
#show vPZ/3.
#show vCREG_PLUS/3.
#show vPOFF_PLUS/3.
#show vCREG_MINUS/3.
#show vPOFF_MINUS/3.

#show vC_P/3.
#show vC_M/3. 
#show vE_P1/3.
#show vE_M1/3.
#show vS_P1/3.
#show vS_M1/3.

#show time/1.
#show date/1.


