import unittest
from pathlib import Path
import sys
import os
import yaml

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

import blcrypt

class TestValidation(unittest.TestCase):
    def test_validate_data_valid_character(self):
        valid_data = {
            'state': {
                'char_name': 'Test',
                'experience': []
            }
        }
        # Should not raise exception
        blcrypt.validate_decrypted_data(valid_data)

    def test_validate_data_valid_profile(self):
        valid_data = {
            'shared': {
                'inventory': {}
            }
        }
        # Should not raise exception
        blcrypt.validate_decrypted_data(valid_data)

    def test_validate_data_invalid_format(self):
        invalid_data = ["not", "a", "dict"]
        with self.assertRaises(ValueError) as cm:
            blcrypt.validate_decrypted_data(invalid_data)
        self.assertIn("Decrypted data must be a dictionary", str(cm.exception))

    def test_validate_data_missing_keys(self):
        invalid_data = {'wrong_key': 123}
        with self.assertRaises(ValueError) as cm:
            blcrypt.validate_decrypted_data(invalid_data)
        self.assertIn("Missing expected keys", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
