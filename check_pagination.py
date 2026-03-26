"""
Zkontroluj, zda je třeba stránkování a vypis všechny dostupné módy
"""

import requests
import json

api_url = "https://api.ficsit.app/v1/mods"

try:
    # Zkusit s různými hodnotami limitu
    for limit in [10, 50, 100, 500, 1000]:
        print(f"\nPokus s limit={limit}:")
        response = requests.get(api_url, params={"limit": limit}, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        mods_count = len(data.get("data", []))
        print(f"  Získáno {mods_count} módů")
        
        if limit == 1000:
            # Vypis všechny názvy módů
            print(f"\n  Všech {mods_count} názvů módů:")
            for mod in data.get("data", []):
                print(f"    - {mod.get('name')}")

except Exception as e:
    print(f"Chyba: {e}")
    import traceback
    traceback.print_exc()
