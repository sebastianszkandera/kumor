"""
Hledej módy Satisfactory na mod.io (komplexnější API)
"""

import requests
import json

# mod.io používá ID hry 3959 pro Satisfactory
api_url = "https://api.mod.io/v1/games/3959/mods"

target_mods = [
    "Refined Power",
    "Satisfactory Mod Loader",
    "Infinite Zoop",
    "Infinite Nudge",
    "MK++",
    "Content Lib"
]

try:
    print("Získávám módy z mod.io...")
    response = requests.get(api_url, params={"_limit": 100}, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    mods = data.get("data", [])
    
    print(f"Nalezeno {len(mods)} celkových módů na mod.io\n")
    print("Hledám vaše cílové módy:\n")
    
    for target in target_mods:
        print(f"🔍 Hledám: {target}")
        found = False
        
        for mod in mods:
            mod_name = mod.get("name", "").lower()
            if target.lower() in mod_name or target.lower().replace(" ", "") in mod_name.replace(" ", ""):
                print(f"  ✅ Nalezeno: {mod.get('name')}")
                print(f"     ID: {mod.get('id')}")
                print(f"     URL: {mod.get('profile_url')}")
                found = True
                break
        
        if not found:
            print(f"  ❌ Nenalezeno")
    
    print(f"\n\nVšechny dostupné módy na mod.io (prvních 100):")
    for mod in mods:
        print(f"  - {mod.get('name')}")

except Exception as e:
    print(f"Chyba: {e}")
    import traceback
    traceback.print_exc()
