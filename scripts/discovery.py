import os
from pathlib import Path

def find_save_directory(platform_id=None):
    """
    Automatically locates the Borderlands 4 save directory.
    Returns a Path object or None if not found.
    """
    user_profile = os.environ.get('USERPROFILE')
    if not user_profile:
        return None
        
    base_user_path = Path(user_profile)
    
    # Potential locations for "My Games\Borderlands 4\Saved\SaveGames"
    potential_roots = [
        base_user_path / "Documents",
        base_user_path / "OneDrive" / "Documents"
    ]
    
    save_games_subpath = Path("My Games") / "Borderlands 4" / "Saved" / "SaveGames"
    
    for root in potential_roots:
        candidate_path = root / save_games_subpath
        if candidate_path.exists():
            if platform_id:
                # If ID is provided, look for the deep path
                deep_path = candidate_path / platform_id / "Profiles" / "client"
                if deep_path.exists():
                    return deep_path
            return candidate_path
            
    return None
