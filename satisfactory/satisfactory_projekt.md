# Satisfactory Mod Notifier

## Popis a cíl projektu
Aplikace sleduje dostupnost modů pro hru Satisfactory. Cílem je pomoci uživateli spravovat seznam sledovaných modů a získat upozornění na změnu jejich stavu.

## Popis funkcionality programu
- Zobrazení seznamu sledovaných modů
- Označení modu jako dostupný nebo nedostupný
- Zobrazení logu změn stavu modů
- Uložení stavu modů do `mod_status.json`
- Test notifikací přes příkazový interface

## Technická část
- `plyer` pro zobrazení desktopových notifikací
- `json` pro ukládání stavu modů
- Skript `update_notifier.py` zpracovává příkazy jako `status`, `available`, `unavailable`, `add`, `remove`, `test`
- Lokalní sledování statusu bez přímého přístupu na vzdálený server

## Spuštění
```bash
pip install -r satisfactory\requirements.txt
python satisfactory\update_notifier.py status
```

## Poznámky
Projekt je navržen jako jednoduchý nástroj pro manuální aktualizaci stavu modů. V praxi je vhodné rozšířit automatizaci kontroly dostupnosti na webu.