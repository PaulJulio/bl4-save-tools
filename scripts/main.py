import sys
import os
from pathlib import Path

# Add the current directory to the path so it can find discovery.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from discovery import find_save_directory

def main():
    save_dir = find_save_directory()
    if not save_dir:
        print("Error: Could not locate Borderlands 4 save directory.")
        sys.exit(1)
        
    print(f"Located save directory: {save_dir}")
    print("\nAvailable save files:")
    
    # The discovery script might return the root SaveGames or the deep client folder
    # Let's search recursively for .sav files from the discovered root
    sav_files = sorted(list(save_dir.rglob("*.sav")))
    
    if not sav_files:
        print("No .sav files found.")
    else:
        for f in sav_files:
            print(f"- {f.name} ({f.stat().st_size} bytes)")
            
if __name__ == "__main__":
    main()
