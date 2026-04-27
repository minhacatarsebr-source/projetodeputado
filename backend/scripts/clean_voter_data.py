# backend/scripts/clean_voter_data.py
"""
Limpa e padroniza a base de eleitores do Excel.
Saída: data/voters_clean.csv com colunas: name, phone_e164, city, email
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import pandas as pd
import argparse

PHONE_ALIASES = ["telefone", "celular", "whatsapp", "fone", "tel", "phone"]
NAME_ALIASES  = ["nome", "name", "candidato", "eleitor"]
CITY_ALIASES  = ["municipio", "cidade", "city", "município"]
EMAIL_ALIASES = ["email", "e-mail", "correio"]

def normalize_phone(raw) -> str | None:
    if raw is None:
        return None
    digits = re.sub(r"\D", "", str(raw))
    if digits.startswith("55"):
        digits = digits[2:]
    if len(digits) not in (10, 11):
        return None
    if len(digits) == 10:
        digits = digits[:2] + "9" + digits[2:]
    return "55" + digits

def detect_columns(df: pd.DataFrame) -> dict:
    lower_cols = {c.lower().strip(): c for c in df.columns}
    result = {}
    for field, aliases in [
        ("name",  NAME_ALIASES),
        ("phone", PHONE_ALIASES),
        ("city",  CITY_ALIASES),
        ("email", EMAIL_ALIASES),
    ]:
        for alias in aliases:
            if alias in lower_cols:
                result[field] = lower_cols[alias]
                print(f"  detect_columns: '{field}' → '{lower_cols[alias]}'")
                break
    return result

def clean_dataframe(df: pd.DataFrame, cols: dict) -> pd.DataFrame:
    out = pd.DataFrame()
    out["name"]  = df[cols["name"]].fillna("").str.strip()
    out["phone_e164"] = df[cols["phone"]].apply(normalize_phone)
    out["city"]  = df[cols.get("city", "")].fillna("") if cols.get("city") else ""
    out["email"] = df[cols.get("email", "")].fillna("") if cols.get("email") else ""
    out = out.dropna(subset=["phone_e164"])
    out = out.drop_duplicates(subset=["phone_e164"])
    out = out[out["name"] != ""]
    return out.reset_index(drop=True)

def main(input_path: str, output_path: str):
    print(f"Lendo {input_path}...")
    df = pd.read_excel(input_path)
    print(f"  {len(df)} linhas brutas")

    cols = detect_columns(df)
    required = {"name", "phone"}
    missing = required - set(cols.keys())
    if missing:
        raise ValueError(f"Colunas não encontradas: {missing}. Colunas do arquivo: {list(df.columns)}")

    clean = clean_dataframe(df, cols)
    print(f"  {len(clean)} linhas após limpeza")

    dirpart = os.path.dirname(output_path)
    if dirpart:
        os.makedirs(dirpart, exist_ok=True)
    clean.to_csv(output_path, index=False)
    print(f"Salvo em {output_path}")
    return clean

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/voters.xlsx")
    parser.add_argument("--output", default="data/voters_clean.csv")
    args = parser.parse_args()
    main(args.input, args.output)
