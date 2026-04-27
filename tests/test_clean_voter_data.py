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
