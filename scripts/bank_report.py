import os
from pathlib import Path
from discovery import find_save_directory

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

def main():
    pass

if __name__ == "__main__":
    main()
