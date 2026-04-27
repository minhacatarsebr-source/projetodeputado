# backend/scripts/import_to_kommo.py
"""
Importa contatos limpos (voters_clean.csv) para o Kommo CRM em lotes de 250.
Idempotente: contatos com mesmo telefone não são duplicados pelo Kommo.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import time
import requests
import argparse
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

KOMMO_SUBDOMAIN = os.getenv("KOMMO_SUBDOMAIN")
KOMMO_TOKEN     = os.getenv("KOMMO_TOKEN")
BATCH_SIZE      = 250

def build_contact_payload(row: dict) -> dict:
    phone = "+" + row["phone_e164"]
    custom_fields = [
        {"field_code": "PHONE", "values": [{"value": phone, "enum_code": "WORK"}]},
    ]
    if row.get("email"):
        custom_fields.append(
            {"field_code": "EMAIL", "values": [{"value": row["email"], "enum_code": "WORK"}]}
        )
    payload = {"name": row["name"], "custom_fields_values": custom_fields}
    if row.get("city"):
        payload["_city"] = row["city"]
    return payload

def chunk_list(lst: list, size: int) -> list[list]:
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def import_contacts(csv_path: str):
    if not KOMMO_SUBDOMAIN or not KOMMO_TOKEN:
        raise EnvironmentError("KOMMO_SUBDOMAIN e KOMMO_TOKEN precisam estar no .env")

    url = f"https://{KOMMO_SUBDOMAIN}.kommo.com/api/v4/contacts"
    headers = {
        "Authorization": f"Bearer {KOMMO_TOKEN}",
        "Content-Type": "application/json",
    }

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"{len(rows)} contatos para importar")

    payloads = [build_contact_payload(r) for r in rows]
    batches  = chunk_list(payloads, BATCH_SIZE)
    total_ok = 0

    for i, batch in enumerate(batches, 1):
        print(f"  Lote {i}/{len(batches)} ({len(batch)} contatos)...", end=" ")
        resp = requests.post(url, json=batch, headers=headers)
        if resp.status_code in (200, 201):
            imported = len(resp.json().get("_embedded", {}).get("contacts", []))
            total_ok += imported
            print(f"OK ({imported} importados)")
        else:
            print(f"ERRO {resp.status_code}: {resp.text[:200]}")
        time.sleep(0.5)

    print(f"\nTotal importado: {total_ok}/{len(rows)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/voters_clean.csv")
    args = parser.parse_args()
    import_contacts(args.input)
