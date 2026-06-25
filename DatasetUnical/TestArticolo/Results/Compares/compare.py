import xlwings as xw
from pathlib import Path
import re

# ======================
# CONFIG
# ======================
GREEDY_DIR = Path("greedy")
MILP_DIR = Path("milp")
ASP_FILE = Path("asp") / "analysis.xlsx"

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}")

# ======================
# UTILS
# ======================
def extract_date(name):
    m = DATE_PATTERN.match(name)
    return m.group(0) if m else None


def map_files(folder):
    files = {}
    for f in folder.glob("*.xlsx"):
        date = extract_date(f.name)
        if date:
            files[date] = f
    return files


# ======================
# MAIN
# ======================
def main():

    greedy_files = map_files(GREEDY_DIR)
    milp_files = map_files(MILP_DIR)

    common_dates = sorted(set(greedy_files) & set(milp_files))

    if not common_dates:
        print("Nessuna data comune trovata")
        return

    # avvia Excel (1 sola istanza)
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False

    results = []

    try:
        asp_wb = app.books.open(str(ASP_FILE))

        for date in common_dates:

            print(f"\n=== {date} ===")

            # =====================
            # OPEN WORKBOOKS
            # =====================
            g_wb = app.books.open(str(greedy_files[date]))
            m_wb = app.books.open(str(milp_files[date]))

            # ASP sheet = data
            if date not in [s.name for s in asp_wb.sheets]:
                print(f"ASP sheet mancante: {date}")
                g_wb.close()
                m_wb.close()
                continue

            g_ws = g_wb.sheets[0]   # oppure .sheets["Sheet1"]
            m_ws = m_wb.sheets[0]
            a_ws = asp_wb.sheets[date]

            # =====================
            # LETTURA CELLE (ESEMPIO)
            # =====================

            # esempio colonne tipiche
            greedy_discharge = g_ws.range("B26").value
            milp_discharge   = m_ws.range("H26").value
            asp_discharge    = a_ws.range("M27").value


            print("Discharge:")
            print("  greedy:", greedy_discharge)
            print("  milp  :", milp_discharge)
            print("  asp   :", asp_discharge)



            results.append({
                "date": date,
                "greedy_discharge": greedy_discharge,
                "milp_discharge": milp_discharge,
                "asp_discharge": asp_discharge,
            })

            # chiudi file per evitare memory leak
            g_wb.close()
            m_wb.close()

        asp_wb.close()

    finally:
        app.quit()

    # ======================
    # OUTPUT
    # ======================
    import pandas as pd

    df = pd.DataFrame(results)
    df.to_excel("confronto.xlsx", index=False)

    print("\nCreato: confronto.xlsx")


if __name__ == "__main__":
    main()