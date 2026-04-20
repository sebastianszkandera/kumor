# Clicker Simulator

## Popis a cíl projektu
Projekt vytváří jednoduchou GUI hru typu clicker, která počítá kliknutí a zobrazuje vtipné zprávy. Cílem je nasimulovat základní herní mechanismus s grafickým rozhraním a logikou pro náhodné zprávy.

## Popis funkcionality programu
- Zobrazuje tlačítko „Click Me!“
- Po stisknutí se zvětší počet kliknutí
- Při prvním kliknutí se zobrazí speciální zpráva
- Každých 10 kliknutí se otevře nové okno se zprávou
- Zprávy se opakují až po vyčerpání všech dostupných textů

## Technická část
- `tkinter` pro GUI
- `random` pro náhodný výběr zpráv
- Zprávy se vybírají z poolu a po vyčerpání se resetují
- Vnitřní funkce: `show_message_window`, `get_random_message`, `on_click`

## Spuštění
```bash
python clicker_simulator\clicker_simulator.py
```

## Poznámky
Kód obsahuje jednoduchou logiku pro správu stavu kliknutí a pro zabránění opakování stejných zpráv po sobě. Doporučeno doplnit další varianty zpráv a vylepšit GUI.