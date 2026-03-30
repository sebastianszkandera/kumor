"""
Úplná diagnostika odezvy ficsit.app API
"""

import requests
import json

api_url = "https://api.ficsit.app/v1/mods"

try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    print("Úplná odezva API:")
    print(json.dumps(data, indent=2)[:2000])
    
    print("\n" + "="*50)
    print("Hledání našich cílových módů:")
    print("="*50)
    
    mods = data.get("data", [])
    target_mods = ["Refined Power", "Satisfactory Mod Loader", "Infinite Zoop", "Infinite Nudge", "MK++", "Content Lib"]
    
    for target in target_mods:
        print(f"\n🔍 Hledám: {target}")
        found = False
        
        for mod in mods:
            mod_name = mod.get("name", "").lower()
            if target.lower() in mod_name:
                print(f"  ✅ Nalezeno: {mod.get('name')}")
                print(f"     Úplná struktura módu:")
                print(json.dumps(mod, indent=6)[:800])
                found = True
                break
        
        if not found:
            print(f"  ❌ V API nenalezeno")

except Exception as e:
    print(f"Chyba: {e}")
    import traceback
    traceback.print_exc()
