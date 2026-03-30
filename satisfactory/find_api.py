"""
Prozkoumej ficsit.app API a najdi správný endpoint
"""

import requests
import json

# Zkus různé endpointy
endpoints = [
    "https://api.ficsit.app/mods",
    "https://ficsit.app/api/mods",
    "https://api.ficsit.app/v1/mods",
    "https://api.mod.io/v1/games/3959/mods",  # mod.io API (používáno některými správci módů)
]

for url in endpoints:
    print(f"\nPokusím se: {url}")
    try:
        response = requests.get(url, timeout=5)
        print(f"  Stav: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ ÚSPĚCH!")
            print(f"  Klíče: {list(data.keys())[:5]}")
            break
        else:
            print(f"  ❌ Chyba")
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:50]}")

# Zkusit i graphql endpoint
print("\n\nPokušuji se o GraphQL endpoint:")
graphql_url = "https://api.ficsit.app/graphql"
query = {
    "query": """
    {
      getMods(first: 5) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
}

try:
    response = requests.post(graphql_url, json=query, timeout=5)
    print(f"  Stav: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ ÚSPĚCH!")
        print(f"  Data: {json.dumps(data, indent=2)[:500]}")
except Exception as e:
    print(f"  ❌ {type(e).__name__}: {str(e)[:50]}")
