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
