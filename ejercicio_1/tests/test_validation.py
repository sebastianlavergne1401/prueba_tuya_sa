import sys
import os
# Añadir src al path para poder importar utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import validate_phone

# Pruebas unitarias para validate_phone
def test_valid_mobile():
    is_valid, res = validate_phone("3101234567")
    assert is_valid is True
    assert res == "+573101234567"

def test_international_prefix():
    is_valid, res = validate_phone("+57 311 987 6543")
    assert is_valid is True
    assert res == "+573119876543"

def test_invalid_short():
    is_valid, res = validate_phone("12345")
    assert is_valid is False
    assert res == "Longitud insuficiente"

def test_null_value():
    is_valid, res = validate_phone(None)
    assert is_valid is False
    assert "Vacio o Nulo" in res

def test_empty_value():
    is_valid, res = validate_phone("")
    assert is_valid is False
    assert "Vacio o Nulo" in res