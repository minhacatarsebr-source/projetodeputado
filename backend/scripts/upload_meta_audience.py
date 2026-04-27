# backend/scripts/upload_meta_audience.py
"""
Cria uma Custom Audience no Meta Ads e sobe os telefones hasheados.
Idempotente: se a audiência já existe com o mesmo nome, reutiliza.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import hashlib
import time
import argparse
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

ACCESS_TOKEN    = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID   = os.getenv("META_AD_ACCOUNT_ID")
AUDIENCE_NAME   = os.getenv("META_AUDIENCE_NAME", "Eleitores Base 2022")
BATCH_SIZE      = 10_000

def hash_phone(phone_e164: str) -> str:
    return hashlib.sha256(phone_e164.encode()).hexdigest()

def build_user_payload(phones: list[str]) -> dict:
    return {
        "schema": ["PHONE"],
        "data": [[hash_phone(p)] for p in phones],
    }

def get_or_create_audience(account: AdAccount) -> str:
    audiences = account.get_custom_audiences(fields=["id", "name"])
    for aud in audiences:
        if aud["name"] == AUDIENCE_NAME:
            print(f"Reutilizando audiência existente: {aud['id']}")
            return aud["id"]

    audience = account.create_custom_audience(params={
        "name": AUDIENCE_NAME,
        "subtype": "CUSTOM",
        "description": "Base de eleitores 2022 importada do CRM",
        "customer_file_source": "USER_PROVIDED_ONLY",
    })
    print(f"Audiência criada: {audience['id']}")
    return audience["id"]

def upload_audience(csv_path: str):
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)
    account  = AdAccount(AD_ACCOUNT_ID)
    aud_id   = get_or_create_audience(account)
    audience = CustomAudience(aud_id)

    with open(csv_path, newline="", encoding="utf-8") as f:
        phones = [row["phone_e164"] for row in csv.DictReader(f) if row.get("phone_e164")]

    print(f"{len(phones)} telefones para subir")

    batches = [phones[i:i+BATCH_SIZE] for i in range(0, len(phones), BATCH_SIZE)]
    for i, batch in enumerate(batches, 1):
        print(f"  Lote {i}/{len(batches)} ({len(batch)} telefones)...", end=" ")
        payload = build_user_payload(batch)
        audience.create_users_replace(params={"payload": payload}) if i == 1 else \
        audience.create_users(params={"payload": payload})
        print("OK")
        time.sleep(1)

    print(f"\nAudiência {AUDIENCE_NAME} atualizada com {len(phones)} telefones.")
    print(f"ID da audiência: {aud_id} — use para criar Lookalike no Ads Manager.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/voters_clean.csv")
    args = parser.parse_args()
    upload_audience(args.input)
