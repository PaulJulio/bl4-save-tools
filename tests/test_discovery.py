import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import os
import sys

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from discovery import find_save_directory

class TestDiscovery(unittest.TestCase):
    def setUp(self):
        self.mock_userprofile = r"C:\Users\TestUser"
        self.standard_path = Path(self.mock_userprofile) / "Documents" / "My Games" / "Borderlands 4" / "Saved" / "SaveGames"
        self.onedrive_path = Path(self.mock_userprofile) / "OneDrive" / "Documents" / "My Games" / "Borderlands 4" / "Saved" / "SaveGames"

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_find_save_directory_standard(self, mock_get, mock_exists):
        # Setup mock for standard path
        mock_get.return_value = self.mock_userprofile
        
        # We need to mock exists for the path we expect
        def exists_side_effect(path):
            return str(path) == str(self.standard_path)
            
        mock_exists.side_effect = exists_side_effect
        
        result = find_save_directory()
        self.assertEqual(result, self.standard_path)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_find_save_directory_onedrive(self, mock_get, mock_exists):
        # Setup mock for OneDrive path
        mock_get.return_value = self.mock_userprofile
        
        def exists_side_effect(path):
            # Fail standard path, succeed on OneDrive
            if "OneDrive" in str(path):
                return True
            return False
            
        mock_exists.side_effect = exists_side_effect
        
        result = find_save_directory()
        self.assertEqual(result, self.onedrive_path)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_find_save_directory_not_found(self, mock_get, mock_exists):
        mock_get.return_value = self.mock_userprofile
        mock_exists.return_value = False
        
        result = find_save_directory()
        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_find_save_directory_with_id(self, mock_get, mock_exists):
        mock_get.return_value = self.mock_userprofile
        steam_id = "76561197967455859"
        expected_path = self.standard_path / steam_id / "Profiles" / "client"
        
        def exists_side_effect(path):
            return str(path) == str(expected_path) or str(path) == str(self.standard_path)
            
        mock_exists.side_effect = exists_side_effect
        
        result = find_save_directory(steam_id)
        self.assertEqual(result, expected_path)

if __name__ == '__main__':
    unittest.main()
