# Dokumentace pro Weather App

## Popis aplikace

Tato aplikace je jednoduchá desktopová aplikace pro zobrazení počasí, napsaná v Pythonu pomocí knihovny Tkinter. Aplikace umožňuje uživatelům vyhledávat počasí pro různá města nebo lokace po celém světě a zobrazuje aktuální počasí spolu s 5denní předpovědí.

## Hlavní funkce

- **Vyhledávání počasí**: Zadejte název města nebo lokace a aplikace načte aktuální počasí a předpověď.
- **Jednotky teploty**: Přepínání mezi stupni Celsia (°C) a Fahrenheita (°F).
- **Historie vyhledávání**: Ukládá posledních 20 vyhledávaných lokalit pro rychlé opětovné vyhledání.
- **Oblíbené lokality**: Umožňuje přidat lokality do oblíbených pro snadný přístup.
- **Více uživatelů**: Každý uživatel má svůj vlastní soubor s daty (historie a oblíbené).
- **Cache**: Data se ukládají do cache na 15 minut pro rychlejší načítání.
- **5denní předpověď**: Zobrazuje počasí na následujících 5 dní včetně maximálních a minimálních teplot.

## Jak spustit aplikaci

1. Ujistěte se, že máte nainstalovaný Python (verze 3.6 nebo vyšší).
2. Nainstalujte potřebné závislosti:
   ```
   pip install requests
   ```
   (PIL/Pillow je volitelný pro pokročilé ikony, ale aplikace funguje i bez něj.)
3. Spusťte aplikaci:
   ```
   python weather_app.py
   ```

## Závislosti

- **requests**: Pro HTTP požadavky na API.
- **tkinter**: Součást standardní knihovny Pythonu (není potřeba instalovat).
- **PIL (Pillow)**: Volitelný pro zobrazení ikon počasí (aktuálně se používá textový popis).

## Používaná API

Aplikace využívá bezplatná API bez nutnosti registračního klíče:

- **Open-Meteo**: Pro data o počasí (https://open-meteo.com/).
- **Nominatim (OpenStreetMap)**: Pro geokódování lokalit (převod názvu města na souřadnice).

## Struktura souborů

- `weather_app.py`: Hlavní soubor aplikace.
- `weather_app_default.json`: Výchozí soubor s daty pro uživatele "default".
- `weather_app_[uživatel].json`: Soubory s daty pro jednotlivé uživatele (např. `weather_app_john.json`).

## Poznámky

- Aplikace ukládá data do JSON souborů ve stejném adresáři.
- Cache se používá pro zrychlení opakovaných vyhledávání.
- V případě chyb sítě nebo neplatné lokace zobrazí aplikace chybovou zprávu.
- Aplikace podporuje více uživatelů, každý s vlastní historií a oblíbenými lokalitami.

## Autor

Tato aplikace byla vytvořena jako ukázkový projekt pro demonstraci práce s API a GUI v Pythonu.