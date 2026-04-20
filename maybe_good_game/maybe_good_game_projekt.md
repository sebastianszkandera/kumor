# Maybe Good Game

## Popis a cíl projektu
Jednoduchá demonstrační hra vytvořená v `pygame`. Cílem je ukázat základní vykreslování grafiky v okně a jednoduchou herní smyčku.

## Popis funkcionality programu
- Spustí full-screen `pygame` okno
- Vykreslí zelené pozadí
- Nakreslí horu a stromy v krajinném stylu
- Zachytává událost `QUIT` pro ukončení aplikace

## Technická část
- `pygame` pro se správu okna a grafiky
- Funkce vykresluje polygony pro hory a kruhy pro koruny stromů
- Vizuální obsah je statický, zelený les a hory
- Hlavní smyčka zpracovává události a obnovuje obrazovku

## Spuštění
```bash
pip install pygame
python maybe_good_game\game.py
```

## Poznámky
Projekt je vhodný jako základ pro další rozšíření do interaktivní hry. Doporučeno přidat ovládání postavy, kolize nebo animace.