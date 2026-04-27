# backend/scripts/run_voter_pipeline.py
"""
Orquestra o pipeline completo: Excel → CSV limpo → Kommo → Meta Audience.
Execute: python backend/scripts/run_voter_pipeline.py --input data/voters.xlsx
"""

import sys, os, argparse, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_CSV = os.path.join(BASE, "..", "data", "voters_clean.csv")

def run(cmd: list[str], label: str):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, check=True)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Caminho para o arquivo Excel")
    parser.add_argument("--skip-kommo",  action="store_true")
    parser.add_argument("--skip-meta",   action="store_true")
    args = parser.parse_args()

    run(
        [sys.executable, os.path.join(BASE, "scripts", "clean_voter_data.py"),
         "--input", args.input, "--output", CLEAN_CSV],
        "PASSO 1/3: Limpeza da base Excel"
    )

    if not args.skip_kommo:
        run(
            [sys.executable, os.path.join(BASE, "scripts", "import_to_kommo.py"),
             "--input", CLEAN_CSV],
            "PASSO 2/3: Importação para Kommo CRM"
        )
    else:
        print("\n[PASSO 2/3 ignorado: --skip-kommo]")

    if not args.skip_meta:
        run(
            [sys.executable, os.path.join(BASE, "scripts", "upload_meta_audience.py"),
             "--input", CLEAN_CSV],
            "PASSO 3/3: Upload Meta Custom Audience"
        )
    else:
        print("\n[PASSO 3/3 ignorado: --skip-meta]")

    print("\n✓ Pipeline concluído.")

if __name__ == "__main__":
    main()
