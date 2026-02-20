import os
from pathlib import Path
from discovery import find_save_directory
from blcrypt import decrypt_sav_to_yaml

def find_profile_save():
    """
    Locates the profile.sav file.
    """
    save_dir = find_save_directory()
    if not save_dir:
        return None
        
    for root, dirs, files in os.walk(save_dir):
        if "profile.sav" in files:
            return Path(root) / "profile.sav"
            
    return None

def get_user_info_from_path(sav_path: Path):
    """
    Extracts User ID and Platform from the save path.
    Expected structure: .../SaveGames/<user_id>/Profiles/client/profile.sav
    """
    # Parent of 'profile.sav' is 'client'
    # Parent of 'client' is 'Profiles'
    # Parent of 'Profiles' is <user_id>
    user_id = sav_path.parent.parent.parent.name
    
    # Simple heuristic: Steam IDs are 17-digit integers
    if user_id.isdigit() and len(user_id) >= 16:
        return user_id, "steam"
    else:
        return user_id, "epic"

def decrypt_profile(sav_path: Path):
    """
    Decrypts the profile save and returns the YAML bytes.
    """
    user_id, platform = get_user_info_from_path(sav_path)
    return decrypt_sav_to_yaml(sav_path, user_id, platform)

def main():
    pass

if __name__ == "__main__":
    main()
