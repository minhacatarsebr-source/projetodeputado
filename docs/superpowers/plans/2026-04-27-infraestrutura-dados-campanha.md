# Infraestrutura de Dados — Campanha Deputado SP 2026

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pipeline completo: Excel de eleitores → limpeza → Kommo CRM → Meta Custom Audience, habilitando lookalikes e retargeting desde o primeiro dia de campanha.

**Architecture:** Três scripts Python independentes em `backend/scripts/`, orquestrados por um runner. Cada script é idempotente — pode ser re-executado sem duplicar dados. O script de limpeza gera um CSV intermediário limpo que os demais consomem.

**Tech Stack:** Python 3.11, pandas, requests, facebook-business SDK (já instalado), python-dotenv, pytest

---

## Configuração de ambiente

Antes de começar, adicionar ao `backend/.env`:

```
# Já existentes:
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_...

# Adicionar:
KOMMO_SUBDOMAIN=seu-subdominio        # ex: "deputadofulano" → deputadofulano.kommo.com
KOMMO_TOKEN=seu-token-longa-duracao   # gerado em Kommo → Integrações → API

# Meta audience:
META_AUDIENCE_NAME=Eleitores Base 2022
```

---

## Task 1: Script de limpeza da base Excel

**Files:**
- Create: `backend/scripts/clean_voter_data.py`
- Create: `tests/test_clean_voter_data.py`
- Create: `data/voters_sample.xlsx` (arquivo de amostra para testes)

**Premissa:** O Excel tem colunas com nomes variados. O script detecta automaticamente e padroniza. Colunas esperadas (aceita variações de maiúsculas/acentos): `nome`, `telefone`/`celular`/`whatsapp`, `municipio`/`cidade`, `email` (opcional).

- [ ] **Step 1: Criar arquivo de amostra para testes**

Crie `data/voters_sample.xlsx` manualmente com 10 linhas de dados fictícios com as colunas:
`Nome`, `Celular`, `Municipio`, `Email`

Inclua propositalmente: duplicatas por telefone, telefones com formatação variada (ex: `(11) 99999-1234`, `11999991234`, `+5511999991234`), linhas com telefone vazio.

- [ ] **Step 2: Escrever os testes**

```python
# tests/test_clean_voter_data.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pandas as pd
import pytest
from scripts.clean_voter_data import (
    normalize_phone,
    detect_columns,
    clean_dataframe,
)

def test_normalize_phone_removes_formatting():
    assert normalize_phone("(11) 99999-1234") == "5511999991234"

def test_normalize_phone_already_clean():
    assert normalize_phone("11999991234") == "5511999991234"

def test_normalize_phone_with_country_code():
    assert normalize_phone("+5511999991234") == "5511999991234"

def test_normalize_phone_invalid_returns_none():
    assert normalize_phone("12345") is None
    assert normalize_phone("") is None
    assert normalize_phone(None) is None

def test_detect_columns_finds_phone():
    df = pd.DataFrame(columns=["Nome", "Celular", "Cidade"])
    cols = detect_columns(df)
    assert cols["phone"] == "Celular"

def test_detect_columns_finds_whatsapp():
    df = pd.DataFrame(columns=["nome", "whatsapp", "municipio"])
    cols = detect_columns(df)
    assert cols["phone"] == "whatsapp"

def test_clean_dataframe_removes_duplicates():
    df = pd.DataFrame({
        "nome": ["João", "Maria", "João Dup"],
        "celular": ["11999991111", "11999992222", "11999991111"],
        "municipio": ["SP", "SP", "SP"],
    })
    result = clean_dataframe(df, {"name": "nome", "phone": "celular", "city": "municipio"})
    assert len(result) == 2

def test_clean_dataframe_drops_invalid_phones():
    df = pd.DataFrame({
        "nome": ["João", "Sem Tel"],
        "celular": ["11999991111", "123"],
        "municipio": ["SP", "SP"],
    })
    result = clean_dataframe(df, {"name": "nome", "phone": "celular", "city": "municipio"})
    assert len(result) == 1
```

- [ ] **Step 3: Rodar os testes para confirmar que falham**

```bash
cd /Users/alexsandro/eleitoral_sp
python -m pytest tests/test_clean_voter_data.py -v
```

Esperado: `ImportError` ou `ModuleNotFoundError` — normal, o módulo ainda não existe.

- [ ] **Step 4: Implementar `clean_voter_data.py`**

```python
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

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clean.to_csv(output_path, index=False)
    print(f"Salvo em {output_path}")
    return clean

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/voters.xlsx")
    parser.add_argument("--output", default="data/voters_clean.csv")
    args = parser.parse_args()
    main(args.input, args.output)
```

- [ ] **Step 5: Rodar os testes**

```bash
python -m pytest tests/test_clean_voter_data.py -v
```

Esperado: todos PASS.

- [ ] **Step 6: Testar com o arquivo real**

```bash
cd /Users/alexsandro/eleitoral_sp
python backend/scripts/clean_voter_data.py \
  --input data/voters.xlsx \
  --output data/voters_clean.csv
```

Esperado: imprime contagem de linhas brutas vs. limpas, gera `data/voters_clean.csv`.

- [ ] **Step 7: Commit**

```bash
git add backend/scripts/clean_voter_data.py tests/test_clean_voter_data.py
git commit -m "feat: script de limpeza da base de eleitores Excel"
```

---

## Task 2: Script de importação para Kommo CRM

**Files:**
- Create: `backend/scripts/import_to_kommo.py`
- Create: `tests/test_kommo_import.py`

**API Kommo usada:**
- `POST https://{subdomain}.kommo.com/api/v4/contacts` — até 250 contatos por lote
- Auth: `Authorization: Bearer {KOMMO_TOKEN}`
- Contato com mesmo telefone já existente não é duplicado (verificado via `custom_fields_values`)

- [ ] **Step 1: Escrever os testes**

```python
# tests/test_kommo_import.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from unittest.mock import patch, MagicMock
from scripts.import_to_kommo import build_contact_payload, chunk_list

def test_build_contact_payload_minimal():
    row = {"name": "João Silva", "phone_e164": "5511999991234", "city": "SP", "email": ""}
    payload = build_contact_payload(row)
    assert payload["name"] == "João Silva"
    phone_field = next(f for f in payload["custom_fields_values"] if f["field_code"] == "PHONE")
    assert phone_field["values"][0]["value"] == "+5511999991234"

def test_build_contact_payload_includes_email_when_present():
    row = {"name": "Maria", "phone_e164": "5511888881234", "city": "", "email": "maria@test.com"}
    payload = build_contact_payload(row)
    email_field = next((f for f in payload["custom_fields_values"] if f["field_code"] == "EMAIL"), None)
    assert email_field is not None
    assert email_field["values"][0]["value"] == "maria@test.com"

def test_chunk_list_splits_correctly():
    items = list(range(550))
    chunks = chunk_list(items, 250)
    assert len(chunks) == 3
    assert len(chunks[0]) == 250
    assert len(chunks[1]) == 250
    assert len(chunks[2]) == 50
```

- [ ] **Step 2: Rodar os testes para confirmar que falham**

```bash
python -m pytest tests/test_kommo_import.py -v
```

Esperado: `ImportError` — módulo ainda não existe.

- [ ] **Step 3: Implementar `import_to_kommo.py`**

```python
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
        payload["_city"] = row["city"]  # usado como tag, não campo nativo
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
        time.sleep(0.5)  # respeitar rate limit da API

    print(f"\nTotal importado: {total_ok}/{len(rows)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/voters_clean.csv")
    args = parser.parse_args()
    import_contacts(args.input)
```

- [ ] **Step 4: Rodar os testes**

```bash
python -m pytest tests/test_kommo_import.py -v
```

Esperado: todos PASS.

- [ ] **Step 5: Executar importação real**

```bash
cd /Users/alexsandro/eleitoral_sp
python backend/scripts/import_to_kommo.py --input data/voters_clean.csv
```

Esperado: imprime progresso por lote, total importado ao final. Verificar no painel do Kommo em Contatos.

- [ ] **Step 6: Commit**

```bash
git add backend/scripts/import_to_kommo.py tests/test_kommo_import.py
git commit -m "feat: importacao em lote de eleitores para Kommo CRM"
```

---

## Task 3: Script de Custom Audience no Meta

**Files:**
- Create: `backend/scripts/upload_meta_audience.py`
- Create: `tests/test_meta_audience.py`

**Fluxo:**
1. Cria (ou reutiliza) uma Custom Audience do tipo `CUSTOM` com schema `PHONE`
2. Faz hash SHA256 dos telefones (obrigatório pelo Meta)
3. Sobe em lotes de 10.000 via `/{audience_id}/users`

- [ ] **Step 1: Escrever os testes**

```python
# tests/test_meta_audience.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from scripts.upload_meta_audience import hash_phone, build_user_payload

def test_hash_phone_returns_64_char_hex():
    result = hash_phone("5511999991234")
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)

def test_hash_phone_is_deterministic():
    assert hash_phone("5511999991234") == hash_phone("5511999991234")

def test_hash_phone_different_numbers_differ():
    assert hash_phone("5511999991234") != hash_phone("5511999995678")

def test_build_user_payload_structure():
    phones = ["5511999991234", "5511888881234"]
    payload = build_user_payload(phones)
    assert payload["schema"] == ["PHONE"]
    assert len(payload["data"]) == 2
    assert len(payload["data"][0]) == 1
    assert len(payload["data"][0][0]) == 64  # sha256 hex
```

- [ ] **Step 2: Rodar os testes para confirmar que falham**

```bash
python -m pytest tests/test_meta_audience.py -v
```

Esperado: `ImportError`.

- [ ] **Step 3: Implementar `upload_meta_audience.py`**

```python
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
```

- [ ] **Step 4: Rodar os testes**

```bash
python -m pytest tests/test_meta_audience.py -v
```

Esperado: todos PASS (não faz chamada real à API).

- [ ] **Step 5: Executar upload real**

```bash
cd /Users/alexsandro/eleitoral_sp
python backend/scripts/upload_meta_audience.py --input data/voters_clean.csv
```

Esperado: cria audiência no Meta, sobe telefones hasheados, imprime ID da audiência.
Verificar no Meta Ads Manager → Públicos → "Eleitores Base 2022".

- [ ] **Step 6: Commit**

```bash
git add backend/scripts/upload_meta_audience.py tests/test_meta_audience.py
git commit -m "feat: upload de custom audience Meta com telefones hasheados"
```

---

## Task 4: Runner orquestrador do pipeline

**Files:**
- Create: `backend/scripts/run_voter_pipeline.py`

Executa os 3 scripts em sequência com logs e verificações de saída.

- [ ] **Step 1: Implementar o runner**

```python
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
```

- [ ] **Step 2: Testar o runner ponta a ponta com arquivo de amostra**

```bash
cd /Users/alexsandro/eleitoral_sp
python backend/scripts/run_voter_pipeline.py --input data/voters_sample.xlsx
```

Esperado: executa os 3 passos em sequência com logs de progresso.

- [ ] **Step 3: Commit**

```bash
git add backend/scripts/run_voter_pipeline.py
git commit -m "feat: runner orquestrador do pipeline Excel → Kommo → Meta"
```

---

## Task 5: Criar Lookalike Audience no Meta (passo manual + documentação)

Após o upload da Custom Audience, criar o Lookalike é feito no Ads Manager. Documentar o passo a passo para o arquivo README.

- [ ] **Step 1: No Meta Ads Manager**

1. Acessar **Públicos** → selecionar "Eleitores Base 2022"
2. Clicar em **Criar Público Similar (Lookalike)**
3. Configurar:
   - Local: **Brasil**
   - Tamanho: **1%** (mais similar) para conversão / **3-5%** para awareness
   - Criar 3 públicos simultâneos: 1%, 2%, 3%
4. Aguardar 24-48h para o Meta processar

- [ ] **Step 2: Adicionar instruções ao README existente**

No arquivo `README.md` do projeto, adicionar seção:

```markdown
## Voter Data Pipeline

### Run the full pipeline
```bash
python backend/scripts/run_voter_pipeline.py --input data/voters.xlsx
```

### Run individual steps
```bash
# Only clean
python backend/scripts/clean_voter_data.py --input data/voters.xlsx --output data/voters_clean.csv

# Only Kommo import (needs clean CSV)
python backend/scripts/import_to_kommo.py --input data/voters_clean.csv

# Only Meta upload (needs clean CSV)
python backend/scripts/upload_meta_audience.py --input data/voters_clean.csv
```

### After Meta upload: create Lookalike
1. Ads Manager → Públicos → "Eleitores Base 2022" → Criar Público Similar
2. Brasil, tamanhos 1% / 2% / 3%
3. Aguardar 24-48h
```

- [ ] **Step 3: Commit final**

```bash
git add README.md
git commit -m "docs: instrucoes pipeline de dados e criacao de lookalike Meta"
```

---

## Checklist de verificação pós-execução

Antes de considerar o plano concluído, verificar:

- [ ] `data/voters_clean.csv` gerado com contagem plausível de linhas
- [ ] Contatos aparecem no Kommo CRM em **Contatos** com telefone formatado
- [ ] Audiência "Eleitores Base 2022" aparece no Meta Ads Manager com status "Pronto"
- [ ] Lookalike 1% criado e em processamento
- [ ] Todos os testes passam: `python -m pytest tests/ -v`

---

## Próximos planos

- **Plano B:** Landing page de captura de leads (HTML + Meta Pixel + integração Kommo via webhook)
- **Plano C:** Deploy do `eleitoral_sp` heatmap para uso em alocação de budget por município
