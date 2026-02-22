import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from bank_report import find_profile_save, get_user_info_from_path, decrypt_profile, extract_bank_serials, get_item_info

class TestBankReport(unittest.TestCase):

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

    def test_get_user_info_from_path_steam(self):
        path = Path("C:/SaveGames/76561197967455859/Profiles/client/profile.sav")
        user_id, platform = get_user_info_from_path(path)
        self.assertEqual(user_id, "76561197967455859")
        self.assertEqual(platform, "steam")

    def test_get_user_info_from_path_epic(self):
        path = Path("C:/SaveGames/EpicUser123/Profiles/client/profile.sav")
        user_id, platform = get_user_info_from_path(path)
        self.assertEqual(user_id, "EpicUser123")
        self.assertEqual(platform, "epic")

    def test_get_item_info_grenade_new_cid(self):
        # A serial that would have been identified as a weapon previously
        # mid=252, cid=182, has FW
        serial = '@Ugr$Q9m/)}}!bCryOC4%`bwHU~UrYc'
        category, has_fw = get_item_info(serial)
        self.assertEqual(category, "Grenade Ordnance")
        self.assertTrue(has_fw)

    def test_get_item_info_grenade_old_cid(self):
        # mid=254, cid=92, has FW
        serial = '@Ugr$)Nm/)}}!c2&uNkwXXG&kgj%n?qa00'
        category, has_fw = get_item_info(serial)
        self.assertEqual(category, "Grenade Ordnance")
        self.assertTrue(has_fw)

    def test_get_item_info_heavy(self):
        # mid=252, cid=175
        serial = '@Ugr$K7m/)}}!uZIbzNtl(L(MU$xCV8@plTXa?P#QkHR%KZ'
        category, has_fw = get_item_info(serial)
        self.assertEqual(category, "Heavy Weapon Ordnance")
        self.assertTrue(has_fw)

    def test_get_item_info_firmware_pattern(self):
        # A serial that is short but has a firmware pattern
        # blen = 176
        serial = '@Ugr$Q9m/)}}!bCryOC4%`bwHU~UrYc'
        category, has_fw = get_item_info(serial)
        self.assertTrue(has_fw)

    def test_get_item_info_no_firmware_even_if_long(self):
        # A serial that is long but has no firmware pattern
        # blen = 206
        serial = '@Ugr$fEm/%P$!bk(PLUrm>VNhdGXHct9=^Fq'
        category, has_fw = get_item_info(serial)
        self.assertFalse(has_fw)

if __name__ == '__main__':
    unittest.main()
