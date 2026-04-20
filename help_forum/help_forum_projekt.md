# Help Forum

## Popis a cíl projektu
Tento projekt je jednoduché fórum napsané v Pythonu. Cílem je poskytnout základní rozhraní pro přidávání otázek a odpovědí a jejich ukládání do JSON souboru.

## Popis funkcionality programu
- Vkládání otázek do fóra
- Přidávání odpovědí k existujícím otázkám
- Zobrazení otázek a odpovědí v rozhraní
- Ukládání dat do souboru `forum_data.json`
- Načítání uložených otázek při opětovném spuštění

## Technická část
- `tkinter` pro GUI
- `json` pro ukládání dat
- Logika kontroluje prázdné vstupy a validuje vybranou otázku
- Struktura dat: seznam otázek a odpovědí uložený jako JSON

## Spuštění
```bash
python help_forum\help_forum.py
```

## Poznámky
Projekt je jednoduchý prototyp a neobsahuje pokročilé ověřování ani síťové volání. Všechny údaje se ukládají lokálně do JSON souboru.