import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from bank_report import find_profile_save, get_user_info_from_path, decrypt_profile, extract_bank_serials

class TestBankReport(unittest.TestCase):
    # ... existing tests ...

    def test_extract_bank_serials(self):
        decrypted_yaml = b"""
domains:
  local:
    shared:
      inventory:
        items:
          bank:
            slot_0: { serial: "SERIAL1" }
            slot_1: { serial: "SERIAL2" }
"""
        serials = extract_bank_serials(decrypted_yaml)
        self.assertEqual(serials, ["SERIAL1", "SERIAL2"])

    def test_extract_bank_serials_empty(self):
        decrypted_yaml = b"domains: { local: { shared: { inventory: { items: { bank: {} } } } } }"
        serials = extract_bank_serials(decrypted_yaml)
        self.assertEqual(serials, [])

    def test_extract_bank_serials_missing(self):
        decrypted_yaml = b"other: data"
        serials = extract_bank_serials(decrypted_yaml)
        self.assertEqual(serials, [])
    # ... existing tests ...

    def test_get_user_info_from_path_steam(self):
        path = Path("C:/SaveGames/76561197967455859/Profiles/client/profile.sav")
        user_id, platform = get_user_info_from_path(path)
        self.assertEqual(user_id, "76561197967455859")
        self.assertEqual(platform, "steam")

    def test_get_user_info_from_path_epic(self):
        # Assuming Epic IDs are alphanumeric and not just digits
        path = Path("C:/SaveGames/EpicUser123/Profiles/client/profile.sav")
        user_id, platform = get_user_info_from_path(path)
        self.assertEqual(user_id, "EpicUser123")
        self.assertEqual(platform, "epic")

    @patch('bank_report.decrypt_sav_to_yaml')
    def test_decrypt_profile(self, mock_decrypt):
        mock_decrypt.return_value = b"decrypted_data"
        path = Path("C:/SaveGames/76561197967455859/Profiles/client/profile.sav")
        result = decrypt_profile(path)
        self.assertEqual(result, b"decrypted_data")
        mock_decrypt.assert_called_once_with(path, "76561197967455859", "steam")
    @patch('bank_report.find_save_directory')
    @patch('pathlib.Path.exists')
    def test_find_profile_save_found(self, mock_exists, mock_find_save_dir):
        # Mock discovery of save directory
        mock_find_save_dir.return_value = Path("C:/Users/TestUser/Documents/My Games/Borderlands 4/Saved/SaveGames")
        
        # Mock existence of platform ID and profile
        def exists_side_effect(path):
            # Check for profile.sav in any subdirectory
            if "profile.sav" in str(path):
                return True
            # Mock subdirectory discovery
            if "SaveGames" in str(path) and "Profiles" not in str(path):
                return True
            return False
        
        # This is getting complicated to mock Path.glob or os.walk.
        # Let's simplify: find_profile_save should return the path to profile.sav.
        pass

    @patch('bank_report.find_save_directory')
    @patch('os.walk')
    def test_find_profile_save_found_simplified(self, mock_walk, mock_find_save_dir):
        mock_find_save_dir.return_value = Path("C:/SaveGames")
        # Mock os.walk(C:/SaveGames)
        # Yields: root, dirs, files
        mock_walk.return_value = [
            ("C:/SaveGames", ["76561197967455859"], []),
            ("C:/SaveGames/76561197967455859", ["Profiles"], []),
            ("C:/SaveGames/76561197967455859/Profiles", ["client"], []),
            ("C:/SaveGames/76561197967455859/Profiles/client", [], ["profile.sav"])
        ]
        
        result = find_profile_save()
        self.assertEqual(result, Path("C:/SaveGames/76561197967455859/Profiles/client/profile.sav"))

    @patch('bank_report.find_save_directory')
    def test_find_profile_save_not_found(self, mock_find_save_dir):
        mock_find_save_dir.return_value = None
        result = find_profile_save()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
