import unittest
from pathlib import Path
import sys
import os

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

import blcrypt

class TestEncryption(unittest.TestCase):
    def test_derive_key_steam(self):
        # Known steam ID for testing
        steam_id = "76561197967455859"
        key = blcrypt.derive_key(steam_id, platform="steam")
        self.assertEqual(len(key), 32)
        # We can't easily verify the exact bytes without doing the math, 
        # but we can ensure it's consistent.
        key2 = blcrypt.derive_key(steam_id, platform="steam")
        self.assertEqual(key, key2)

    def test_derive_key_epic(self):
        # Known epic ID (placeholder string)
        epic_id = "epic_user_123"
        key = blcrypt.derive_key(epic_id, platform="epic")
        self.assertEqual(len(key), 32)
        key2 = blcrypt.derive_key(epic_id, platform="epic")
        self.assertEqual(key, key2)
        self.assertNotEqual(key, blcrypt.BASE_KEY)

    def test_derive_key_invalid_platform(self):
        with self.assertRaises(ValueError):
            blcrypt.derive_key("id", platform="unknown")

if __name__ == '__main__':
    unittest.main()
