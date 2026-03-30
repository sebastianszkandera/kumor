"""
Testuj ficsit.app API a podívej se, jaká data jsou dostupná
"""

import requests
import json

api_url = "https://api.ficsit.app"

# Pokus se získat módy
search_url = f"{api_url}/v2/mods"
params = {"limit": 100, "offset": 0}

try:
    response = requests.get(search_url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    print("Struktura odezvy API:")
    print(f"Klíče: {data.keys()}")
    print()
    
    mods = data.get("mods", [])
    print(f"Nalezeno {len(mods)} módů")
    print()
    
    # Zobraz první 3 módy jako příklady
    for i, mod in enumerate(mods[:3]):
        print(f"\nMód {i+1}:")
        print(f"  Název: {mod.get('name')}")
        print(f"  ID: {mod.get('id')}")
        print(f"  Klíče: {mod.keys()}")
        
        versions = mod.get("versions", [])
        if versions:
            print(f"  Dostupné verze: {len(versions)}")
            for j, v in enumerate(versions[:2]):
                print(f"    v{j}: {v.get('version')} - Hra: {v.get('game_version')}")
    
    # Nyní hledej konkrétní módy
    print("\n" + "="*50)
    print("Hledání konkrétních módů:")
    print("="*50)
    
    target_mods = ["Refined Power", "Satisfactory Mod Loader"]
    
    for target in target_mods:
        print(f"\nHledám: {target}")
        found = False
        for mod in mods:
            if target.lower() in mod.get("name", "").lower():
                print(f"  ✅ Nalezeno: {mod.get('name')}")
                print(f"     Verze: {len(mod.get('versions', []))}")
                found = True
                break
        if not found:
            print(f"  ❌ Nenalezeno")

except Exception as e:
    print(f"Chyba: {e}")
