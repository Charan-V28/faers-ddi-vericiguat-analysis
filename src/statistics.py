import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import chi2_contingency

def calculate_disproportionality(a: int, b: int, c: int, d: int) -> dict:
    a_c = a if a > 0 else 0.5
    b_c = b if b > 0 else 0.5
    c_c = c if c > 0 else 0.5
    d_c = d if d > 0 else 0.5

    ror = (a_c * d_c) / (b_c * c_c)
    se_log_ror = np.sqrt((1 / a_c) + (1 / b_c) + (1 / c_c) + (1 / d_c))
    ror_ci_lower = np.exp(np.log(ror) - (1.96 * se_log_ror))
    ror_ci_upper = np.exp(np.log(ror) + (1.96 * se_log_ror))

    prr = (a_c / (a_c + b_c)) / (c_c / (c_c + d_c))

    contingency_table = [[a, b], [c, d]]
    chi2, p_val, _, _ = chi2_contingency(contingency_table, correction=True)

    return {
        "count_a": a,
        "count_b": b,
        "count_c": c,
        "count_d": d,
        "ROR": round(ror, 3),
        "ROR_CI_Lower": round(ror_ci_lower, 3),
        "ROR_CI_Upper": round(ror_ci_upper, 3),
        "PRR": round(prr, 3),
        "Chi2": round(chi2, 3),
        "p_value": round(p_val, 5),
        "signal_detected": bool(ror_ci_lower > 1.0 and a >= 3 and chi2 >= 3.84)
    }

def run_batch_screen():
    project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
    drugs_path = project_root / "data" / "processed" / "etripamil_drugs.csv"
    reacs_path = project_root / "data" / "processed" / "etripamil_reactions.csv"

    drugs_df = pd.read_csv(drugs_path)
    reacs_df = pd.read_csv(reacs_path)

    drugs_df["DRUGNAME_CLEAN"] = drugs_df["DRUGNAME"].fillna("").str.strip().str.upper()
    reacs_df["PT_CLEAN"] = reacs_df["PT"].fillna("").str.strip().str.upper()

    drug_a_pattern = "VERICIGUAT|VERQUVO"
    reaction_pattern = "HYPOTENSION"

    co_drugs = [
        ("Entresto / Sacubitril", "ENTRESTO|SACUBITRIL"),
        ("Furosemide", "FUROSEMIDE"),
        ("Spironolactone", "SPIRONOLACTONE"),
        ("Bisoprolol", "BISOPROLOL"),
        ("Jardiance / Empagliflozin", "JARDIANCE|EMPAGLIFLOZIN")
    ]

    all_cases = set(drugs_df["PRIMARYID"]).union(set(reacs_df["PRIMARYID"]))
    ids_drug_a = set(drugs_df[drugs_df["DRUGNAME_CLEAN"].str.contains(drug_a_pattern, regex=True)]["PRIMARYID"])
    ids_reaction = set(reacs_df[reacs_df["PT_CLEAN"].str.contains(reaction_pattern, regex=True)]["PRIMARYID"])

    summary_rows = []

    print("=" * 65)
    print(f"BATCH INTERACTION SCREENING: VERICIGUAT + CONCOMITANT DRUGS")
    print(f"Target Adverse Event: {reaction_pattern}")
    print("=" * 65)

    for name, pattern in co_drugs:
        ids_drug_b = set(drugs_df[drugs_df["DRUGNAME_CLEAN"].str.contains(pattern, regex=True)]["PRIMARYID"])
        ids_both = ids_drug_a.intersection(ids_drug_b)

        a = len(ids_both.intersection(ids_reaction))
        b = len(ids_both.difference(ids_reaction))
        c = len(ids_reaction.difference(ids_both))
        d = len(all_cases.difference(ids_both.union(ids_reaction)))

        metrics = calculate_disproportionality(a, b, c, d)
        metrics["Concomitant_Drug"] = name
        summary_rows.append(metrics)

        print(f"Drug Pair: Vericiguat + {name}")
        print(f"  2x2 Table: a={a}, b={b}, c={c}, d={d}")
        print(f"  ROR: {metrics['ROR']} (95% CI: [{metrics['ROR_CI_Lower']}, {metrics['ROR_CI_Upper']}])")
        print(f"  Chi2: {metrics['Chi2']} | Signal Detected: {metrics['signal_detected']}")
        print("-" * 65)

    summary_df = pd.DataFrame(summary_rows)
    output_path = project_root / "data" / "processed" / "ddi_signals_summary.csv"
    summary_df.to_csv(output_path, index=False)
    print(f"Saved batch results to {output_path}")

if __name__ == "__main__":
    run_batch_screen()