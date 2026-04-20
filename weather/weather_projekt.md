# Weather App

## Popis a cíl projektu
Aplikace poskytuje vyhledávání počasí pro libovolné město nebo lokaci. Cílem je ukázat práci s API, ukládání historie a oblíbených lokalit v desktopovém GUI.

## Popis funkcionality programu
- Vyhledávání aktuálního počasí podle zadané lokace
- Volba jednotek teploty mezi Celsius a Fahrenheit
- Zobrazení 5denní předpovědi
- Historie vyhledávání a oblíbené lokality
- Práce s více uživateli pomocí samostatných JSON souborů

## Technická část
- `tkinter` pro GUI a `ttk` pro vzhled
- `requests` pro volání Open-Meteo a Nominatim API
- `json` pro ukládání historie a oblíbených
- `glob` pro detekci uživatelských souborů
- Aplikace používá jednoduchý caching a ukládání do souboru `weather_app_default.json`

## Spuštění
```bash
pip install requests
python weather\weather_app.py
```

## Poznámky
V případě chyb sítě nebo neplatné lokace aplikace zobrazí chybovou zprávu. Data pro jednotlivé uživatele se ukládají do `weather_app_[uživatel].json`.