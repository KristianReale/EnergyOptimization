import pandas as pd
import xlwings as xw

app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

try:
    asp_wb = app.books.open("k/asp/asp_analysis.xlsx")
    greedy_wb = app.books.open("k/greedy/greedy_analysis.xlsx")
    milp_wb = app.books.open("k/milp/milp_analysis.xlsx")

    def sheets_by_date(wb):
        return {s.name[:10]: s.name for s in wb.sheets if len(s.name) >= 10}

    asp_map = sheets_by_date(asp_wb)
    greedy_map = sheets_by_date(greedy_wb)
    milp_map = sheets_by_date(milp_wb)

    common_dates = set(asp_map) & set(greedy_map) & set(milp_map)

    results = []

    countBetterKGreedy = 0
    countBetterKMILP = 0
    countBetterKASP = 0

    countWorseKGreedy = 0
    countWorseKMILP = 0
    countWorseKASP = 0

    countKLowerGreedy = 0
    countKLowerMILP = 0
    countKLowerASP = 0

    countWorstSolutionGreedy = 0

    rowsInputs = []

    for date in sorted(common_dates):

        asp_ws = asp_wb.sheets[asp_map[date]]
        greedy_ws = greedy_wb.sheets[greedy_map[date]]
        milp_ws = milp_wb.sheets[milp_map[date]]

        if milp_ws.range("A27").value != "Optimal":
            raise ValueError(
                f"Nella data {date} la soluzione non è ottima"
            )
        EPS = 1e-9

        # FEED-IN
        print("MILP: " + str(milp_ws.range("E26").value))
        print("Greedy " + str(greedy_ws.range("F26").value))
        print("ASP " + str(asp_ws.range("Q27").value))
        if abs(milp_ws.range("E26").value - asp_ws.range("Q27").value) > EPS:
            raise ValueError(
                f"La quantità ESPORTATA non corrisponde nella data {date}"
            )

        # FROM-GRID
        print("MILP: " + str(milp_ws.range("D26").value))
        print("Greedy " + str(greedy_ws.range("G26").value))
        print("ASP " + str(asp_ws.range("R27").value))
        if abs(milp_ws.range("D26").value - asp_ws.range("R27").value) > EPS:
            raise ValueError(
                f"La quantità IMPORTATA non corrisponde nella data {date}"
            )

        # CHARGE
        print("MILP: " + str(milp_ws.range("G26").value))
        print("Greedy " + str(greedy_ws.range("C26").value))
        print("ASP " + str(asp_ws.range("N27").value))
        if abs(milp_ws.range("G26").value - asp_ws.range("N27").value) > EPS:
            raise ValueError(
                f"La quantità CARICATA non corrisponde nella data {date}"
            )
        minChargeValue = round(milp_ws.range("G26").value, 3)

        # DISCHARGE
        print("DISCHARGE MILP: " + str(milp_ws.range("H26").value))
        print("DISCHARGE Greedy " + str(greedy_ws.range("B26").value))
        print("DISCHARGE ASP " + str(asp_ws.range("M27").value))
        if abs(milp_ws.range("H26").value - asp_ws.range("M27").value) > EPS:
            raise ValueError(
                f"La quantità SCARICATA non corrisponde nella data {date}"
            )

        if asp_ws.range("M27").value - greedy_ws.range("B26").value > EPS:
            countWorstSolutionGreedy += 1
        # K
        print("MILP: " + str(milp_ws.range("B28").value))
        print("Greedy " + str(greedy_ws.range("B28").value))
        print("ASP " + str(asp_ws.range("N29").value))
        if abs(milp_ws.range("B28").value - greedy_ws.range("B28").value) > EPS or abs(milp_ws.range("B28").value - asp_ws.range("N29").value) > EPS or abs(greedy_ws.range("B28").value - asp_ws.range("N29").value) > EPS:
            raise ValueError(
                f"Il valore K non corrisponde nella data {date}"
            )
        if milp_ws.range("B28").value > milp_ws.range("B29").value:
            countKLowerMILP += 1

        if asp_ws.range("N29").value > asp_ws.range("N30").value:
            countKLowerASP += 1

        if greedy_ws.range("B28").value > greedy_ws.range("B29").value:
            countKLowerGreedy += 1


        minDischargeValue = round(milp_ws.range("H26").value, 3)
        dischargeValuesMilp = milp_ws.range("H2:H25").value
        kMilp = sum(
            1 for v in dischargeValuesMilp
            if isinstance(v, (int, float)) and v > 0
        )
        print(f"K MILP: {kMilp}")
        dischargeValuesGreedy = greedy_ws.range("B2:B25").value
        kGreedy = sum(
            1 for v in dischargeValuesGreedy
            if isinstance(v, (int, float)) and v > 0
        )
        print(f"K Greedy: {kGreedy}")
        dischargeValuesASP = asp_ws.range("M3:M26").value
        kAsp = sum(
            1 for v in dischargeValuesASP
            if isinstance(v, (int, float)) and v > 0
        )
        print(f"K ASP: {kAsp}")
        kMin = kMilp
        if not (kMilp == kGreedy == kAsp):
            minimo = min(kMilp, kGreedy, kAsp)
            massimo = max(kMilp, kGreedy, kAsp)

            if kMilp == minimo and kGreedy != minimo and kAsp != minimo:
                countBetterKMILP += 1
                print("Best KMILP: " + str(date))
            if kMilp != minimo and kGreedy == minimo and kAsp != minimo:
                countBetterKGreedy += 1
                print("Best KGREEDY: " + str(date))
            if kMilp != minimo and kGreedy != minimo and kAsp == minimo:
                countBetterKASP += 1
                print("Best KASP: " + str(date))

            if kMilp == massimo and kGreedy != massimo and kAsp != massimo:
                countWorseKMILP += 1
                print("Worst KMILP: " + str(date))
            if kMilp != massimo and kGreedy == massimo and kAsp != massimo:
                countWorseKGreedy += 1
                print("Worst KGREEDY: " + str(date))
            if kMilp != massimo and kGreedy != massimo and kAsp == massimo:
                countWorseKASP += 1
                print("Worst KASP: " + str(date))

            kMin = minimo

            '''
            if kMilp == minimo:
                countBetterKMILP += 1

            if kGreedy == minimo:
                countBetterKGreedy += 1

            if kAsp == minimo:
                countBetterKASP += 1
            '''
        rowsInputs.append({
            "Date": date,
            "MinDischarge": minDischargeValue,
            "MinCharge": minChargeValue,
            "K": kMin
        })


    print("Le soluzione corrisponde")
    print(f"Best KMILP COUNT: {countBetterKMILP}")
    print(f"Best GREEDY COUNT: {countBetterKGreedy}")
    print(f"Best ASP COUNT: {countBetterKASP}")
    print(f"Worst KMILP COUNT: {countWorseKMILP}")
    print(f"Worst GREEDY COUNT: {countWorseKGreedy}")
    print(f"Worst ASP COUNT: {countWorseKASP}")

    print(f"Best LOWER KMILP COUNT: {countKLowerMILP}")
    print(f"Best LOWER GREED COUNT: {countKLowerGreedy}")
    print(f"Best LOWER ASP COUNT: {countKLowerASP}")

    print(f"WORST Solution GREEDY COUNT: {countWorstSolutionGreedy}")


    df = pd.DataFrame(rowsInputs)
    df.to_csv("resultsK.csv", index=False)

finally:
    app.quit()

