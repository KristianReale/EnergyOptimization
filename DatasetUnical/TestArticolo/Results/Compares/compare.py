import xlwings as xw

app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

try:
    asp_wb = app.books.open("asp/asp_analysis.xlsx")
    greedy_wb = app.books.open("greedy/greedy_analysis.xlsx")
    milp_wb = app.books.open("milp/milp_analysis.xlsx")

    def sheets_by_date(wb):
        return {s.name[:10]: s.name for s in wb.sheets if len(s.name) >= 10}

    asp_map = sheets_by_date(asp_wb)
    greedy_map = sheets_by_date(greedy_wb)
    milp_map = sheets_by_date(milp_wb)

    common_dates = set(asp_map) & set(greedy_map) & set(milp_map)

    CELLS = ["B2", "C2", "D2"]

    results = []

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
        if abs(milp_ws.range("E26").value - greedy_ws.range("F26").value) > EPS or abs(milp_ws.range("E26").value - asp_ws.range("Q27").value) > EPS or abs(greedy_ws.range("F26").value - asp_ws.range("Q27").value) > EPS:
            raise ValueError(
                f"La quantità ESPORTATA non corrisponde nella data {date}"
            )

        # FROM-GRID
        print("MILP: " + str(milp_ws.range("D26").value))
        print("Greedy " + str(greedy_ws.range("G26").value))
        print("ASP " + str(asp_ws.range("R27").value))
        if abs(milp_ws.range("D26").value - greedy_ws.range("G26").value) > EPS or abs(milp_ws.range("D26").value - asp_ws.range("R27").value) > EPS or abs(greedy_ws.range("G26").value - asp_ws.range("R27").value) > EPS:
            raise ValueError(
                f"La quantità IMPORTATA non corrisponde nella data {date}"
            )

        # DISCHARGE
        print("MILP: " + str(milp_ws.range("H26").value))
        print("Greedy " + str(greedy_ws.range("B26").value))
        print("ASP " + str(asp_ws.range("M27").value))
        if abs(milp_ws.range("H26").value - greedy_ws.range("B26").value) > EPS or abs(milp_ws.range("H26").value - asp_ws.range("M27").value) > EPS or abs(greedy_ws.range("B26").value - asp_ws.range("M27").value) > EPS:
            raise ValueError(
                f"La quantità SCARICATA non corrisponde nella data {date}"
            )

        # CHARGE
        print("MILP: " + str(milp_ws.range("G26").value))
        print("Greedy " + str(greedy_ws.range("C26").value))
        print("ASP " + str(asp_ws.range("N27").value))
        if abs(milp_ws.range("G26").value - greedy_ws.range("C26").value) > EPS or abs(milp_ws.range("G26").value - asp_ws.range("N27").value) > EPS or abs(greedy_ws.range("C26").value - asp_ws.range("N27").value) > EPS:
            raise ValueError(
                f"La quantità CARICATA non corrisponde nella data {date}"
            )



    print("Le soluzione corrisponde")

finally:
    app.quit()

