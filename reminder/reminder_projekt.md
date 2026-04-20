# Reminder

## Popis a cíl projektu
Aplikace slouží jako desktopový plánovač připomínek. Cílem je mít funkční nástroj pro zadání upozornění na konkrétní datum a čas s možností opakování.

## Popis funkcionality programu
- Přidání připomínky s textem, datem a časem
- Volba opakování: žádné, denní, týdenní, měsíční
- Zobrazení seznamu připomínek v GUI
- Uložení připomínek do souboru `reminders.json`
- Zobrazení připomínky pomocí dialogu v přesném okamžiku

## Technická část
- `tkinter` pro GUI
- `json` pro perzistentní uložení připomínek
- `datetime` a `time` pro práci s časem
- Periodická kontrola připomínek pomocí `after(1000, ...)`
- Režimy opakování aktualizují `next_time` pro další spuštění

## Spuštění
```bash
python reminder\reminder.py
```

## Poznámky
Aplikace ukládá stav do `reminders.json`. Pokud dojde k chybě při načítání, vytvoří se nová prázdná databáze připomínek.