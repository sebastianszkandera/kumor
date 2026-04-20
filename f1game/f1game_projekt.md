# F1 Game

## Popis a cíl projektu
Projekt demonstruje načítání a vizualizaci F1 telemetrie pomocí knihovny `fastf1`. Cílem je vytvořit jednoduchou analýzu závodních dat a zobrazit rychlostní profil nejlepšího kola.

## Popis funkcionality programu
- Načte kvalifikační session z konkrétního závodu
- Vybere nejrychlejší kolo konkrétního jezdce (`RUS`)
- Získá telemetrii pro toto kolo
- Vykreslí graf rychlosti v závislosti na vzdálenosti

## Technická část
- `fastf1` pro načtení F1 dat
- `matplotlib` pro vykreslení grafu
- `os` pro správu cesty ke cache
- `fastf1.Cache.enable_cache` pro lokální ukládání dat

## Spuštění
```bash
python f1game\f1game.py
```

## Poznámky
Vyžaduje existující cache adresář. Pokud složka cache neexistuje, vytvořte ji ručně nebo změňte cestu v kódu na platnou adresu. Projekt je vhodný pro další rozšíření analýzy telemetrie a porovnání různých jezdců.