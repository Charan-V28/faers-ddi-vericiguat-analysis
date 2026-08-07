import os
import glob
import pandas as pd

TARGET_DRUG_PATTERNS = ["VERICIGUAT", "VERQUVO"]

def run_ingestion_pipeline(data_dir: str, processed_dir: str):
    drug_files = glob.glob(os.path.join(data_dir, "**", "*DRUG*.txt"), recursive=True)
    reac_files = glob.glob(os.path.join(data_dir, "**", "*REAC*.txt"), recursive=True)

    if not drug_files:
        print(f"No DRUG files found in {data_dir}.")
        return

    print("Step 1: Identifying target case IDs...")
    cols_drug = ["PRIMARYID", "CASEID", "ROLE_COD", "DRUGNAME"]
    target_ids = set()

    for file in drug_files:
        df = pd.read_csv(file, sep="$", usecols=lambda c: c.upper() in cols_drug, dtype=str, low_memory=False)
        df.columns = [c.upper() for c in df.columns]
        df["DRUGNAME_CLEAN"] = df["DRUGNAME"].fillna("").str.strip().str.upper()
        
        pattern = "|".join(TARGET_DRUG_PATTERNS)
        matches = df[df["DRUGNAME_CLEAN"].str.contains(pattern, regex=True)]
        target_ids.update(matches["PRIMARYID"].dropna().unique())

    print(f"Found {len(target_ids)} unique target cases.")

    if not target_ids:
        return

    print("Step 2: Extracting ALL co-administered drugs for these cases...")
    all_drugs_list = []
    for file in drug_files:
        df = pd.read_csv(file, sep="$", usecols=lambda c: c.upper() in cols_drug, dtype=str, low_memory=False)
        df.columns = [c.upper() for c in df.columns]
        df["DRUGNAME_CLEAN"] = df["DRUGNAME"].fillna("").str.strip().str.upper()
        
        # Filter for all drug records matching our target cases
        matched = df[df["PRIMARYID"].isin(target_ids)].copy()
        all_drugs_list.append(matched)

    all_drugs_df = pd.concat(all_drugs_list, ignore_index=True)

    print("Step 3: Extracting reaction records for these cases...")
    cols_reac = ["PRIMARYID", "CASEID", "PT"]
    all_reacs_list = []
    for file in reac_files:
        df = pd.read_csv(file, sep="$", usecols=lambda c: c.upper() in cols_reac, dtype=str, low_memory=False)
        df.columns = [c.upper() for c in df.columns]
        
        matched = df[df["PRIMARYID"].isin(target_ids)].copy()
        all_reacs_list.append(matched)

    all_reacs_df = pd.concat(all_reacs_list, ignore_index=True)

    # Save to disk
    os.makedirs(processed_dir, exist_ok=True)
    all_drugs_df.to_csv(os.path.join(processed_dir, "etripamil_drugs.csv"), index=False)
    all_reacs_df.to_csv(os.path.join(processed_dir, "etripamil_reactions.csv"), index=False)
    print("Ingestion complete! Re-saved updated drug and reaction records.")

if __name__ == "__main__":
    run_ingestion_pipeline("data/raw", "data/processed")