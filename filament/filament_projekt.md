# Filament Cost Counter

## Popis a cíl projektu
Projekt slouží k výpočtu celkových nákladů na 3D tisk filamentu. Cílem je poskytnout přehled nákladů na materiál, elektřinu, údržbu a amortizaci tiskárny.

## Popis funkcionality programu
- Uživatelské rozhraní pro zadání parametrů tisku
- Výpočet ceny filamentu na základě hmotnosti a ceny za kilogram
- Výpočet nákladů na elektřinu podle výkonu tiskárny a času tisku
- Výpočet nákladů na údržbu a amortizaci tiskárny
- Zobrazení celkových nákladů v CZK

## Technická část
- `tkinter` pro GUI
- `forex-python` pro převod měny EUR/CZK
- Logika zahrnuje výpočet nákladů na materiál, elektřinu, údržbu a amortizaci
- Jedná se o front-endovou kalkulačku bez přímých volání externích API kromě měnového převodu

## Spuštění
```bash
pip install forex-python
python filament\filament_cost_counter.py
```

## Poznámky
Projekt vyžaduje internet pro získání aktuálního kurzu EUR/CZK. Amortizace tiskárny se počítá pouze pokud jsou zadány volitelné parametry.