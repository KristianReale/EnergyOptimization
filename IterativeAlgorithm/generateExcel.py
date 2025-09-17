#!/usr/bin/env python3
"""
json_to_excel.py
Legge un file JSON e lo esporta in un Excel contenente:
 - foglio "Variables": tutte le variabili (colonne) allineate per indice (Hour)
 - foglio "Summary": campi top-level (es. computation_time, objective_function)
 - foglio "RawJSON": JSON pretty-printed in una singola cella
 - (opzionale) fogli separati per ogni variabile (--per-var)
Uso:
  python json_to_excel.py input.json output.xlsx
  python json_to_excel.py input.json output.xlsx --per-var
"""

import json
import argparse
import pandas as pd
import math
from collections import Counter

def safe_sheet_name(name: str) -> str:
    # massimo 31 char, rimuove/carica caratteri proibiti
    s = str(name)
    for ch in '[]:*?/\\':
        s = s.replace(ch, '_')
    s = s[:31]
    return s

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to Excel (Variables/Summary/RawJSON).")
    parser.add_argument("input_json", help="File JSON di input")
    parser.add_argument("output_xlsx", nargs='?', default="result.xlsx", help="File Excel di output (default: result.xlsx)")
    parser.add_argument("--per-var", action="store_true", help="Crea un foglio separato per ogni variabile")
    args = parser.parse_args()

    # carica JSON
    with open(args.input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- SUMMARY: prendi tutti i top-level keys tranne 'variables' ---
    summary_items = {}
    for k, v in data.items():
        if k == "variables":
            continue
        # serializza valori non-scalar
        if isinstance(v, (dict, list)):
            summary_items[k] = json.dumps(v)
        else:
            summary_items[k] = v

    # scrivo summary come DataFrame (key, value) per leggibilità
    if summary_items:
        summary_df = pd.DataFrame(list(summary_items.items()), columns=["key", "value"])
    else:
        summary_df = pd.DataFrame(columns=["key", "value"])

    # --- VARIABLES: costruisci tabella allineata per indice (Hour) ---
    variables = data.get("variables", {})
    if not isinstance(variables, dict):
        raise ValueError("Il campo 'variables' nel JSON deve essere un oggetto/dizionario.")

    # trova la lunghezza massima tra le liste (se sono liste) o considera 1 per scalari
    lengths = []
    for k, v in variables.items():
        if isinstance(v, (list, tuple)):
            lengths.append(len(v))
        else:
            lengths.append(1)
    max_len = max(lengths) if lengths else 0

    # costruisci dict per DataFrame, padding con NaN se necessario
    vars_for_df = {}
    for name, vals in variables.items():
        if isinstance(vals, (list, tuple)):
            vals_list = list(vals)
        else:
            # scalar: ripeti il valore per ogni riga
            vals_list = [vals]

        # pad to max_len with NaN
        if len(vals_list) < max_len:
            vals_list = vals_list + [float("nan")] * (max_len - len(vals_list))
        vars_for_df[name] = vals_list

    # crea DataFrame con Hour come prima colonna (1..max_len)
    if max_len > 0:
        df_vars = pd.DataFrame(vars_for_df)
        df_vars.insert(0, "Hour", range(1, max_len + 1))
    else:
        # caso limite: nessuna variabile
        df_vars = pd.DataFrame()

    # --- WRITER: scrive i fogli su Excel ---
    with pd.ExcelWriter(args.output_xlsx, engine="openpyxl") as writer:
        # Variables
        if not df_vars.empty:
            df_vars.to_excel(writer, sheet_name="Variables", index=False)
        else:
            # crea foglio vuoto
            pd.DataFrame().to_excel(writer, sheet_name="Variables", index=False)

        # Summary
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        # Raw JSON (pretty printed in una cella)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        raw_df = pd.DataFrame({"json_pretty": [pretty]})
        # se la stringa è troppo lunga, va comunque in cella; Excel la gestisce
        raw_df.to_excel(writer, sheet_name="RawJSON", index=False)

        # Fogli separati per variabili (opzionale)
        if args.per_var:
            # evitiamo nomi duplicati di fogli; teniamo contatore
            name_counts = Counter()
            for name, vals in vars_for_df.items():
                base = safe_sheet_name(name)
                name_counts[base] += 1
                sheet_name = base if name_counts[base] == 1 else f"{base}_{name_counts[base]}"
                var_df = pd.DataFrame({
                    "Hour": range(1, max_len + 1),
                    "Value": vals
                })
                var_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ Creato: {args.output_xlsx}")
    print("Sheets creati: Variables, Summary, RawJSON" + (", +1 per-variable each" if args.per_var else ""))

if __name__ == "__main__":
    main()
