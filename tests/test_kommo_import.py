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
