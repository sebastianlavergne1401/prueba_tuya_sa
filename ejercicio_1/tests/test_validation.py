import sys
import os
import unittest

# Añadir la carpeta 'src' al path para poder importar utils.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import validate_phone

class TestPhoneValidation(unittest.TestCase):
    
    def test_valid_mobile(self):
        is_valid, res = validate_phone("3101234567")
        self.assertTrue(is_valid)
        self.assertEqual(res, "+573101234567")

    def test_international_prefix(self):
        is_valid, res = validate_phone("+57 311 987 6543")
        self.assertTrue(is_valid)
        self.assertEqual(res, "+573119876543")

    def test_invalid_short(self):
        is_valid, res = validate_phone("12345")
        self.assertFalse(is_valid)
        self.assertEqual(res, "Longitud insuficiente")

    def test_null_value(self):
        is_valid, res = validate_phone(None)
        self.assertFalse(is_valid)
        self.assertIn("Vacio o Nulo", res)

    def test_empty_value(self):
        is_valid, res = validate_phone("")
        self.assertFalse(is_valid)
        self.assertIn("Vacio o Nulo", res)

if __name__ == "__main__":
    unittest.main()