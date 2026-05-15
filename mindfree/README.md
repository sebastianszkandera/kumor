# MindFree

MindFree je cross-platform aplikace pro PC a Android, která pomáhá omezit závislost na sociálních sítích pomocí sledování času, focus režimu a nastavení blokací.

## Funkce
- vestavěný MindFree safe browser pro TikTok, Instagram, YouTube a další weby
- načítání stránek bez trackerů, skriptů a doporučovaných bloků
- plánované blokování webů v desktopových prohlížečích přes hosts soubor
- přepínače pro blokování trackerů, nekonečný scroll, doporučení a notifikace
- focus režim se sledováním produktivního času
- dětský režim s redukcí rizikových prvků
- denní cíl a jednoduché statistiky

## Spuštění na PC
1. Nainstaluj Python 3.13+.
2. Otevři terminál ve složce `mindfree`.
3. Nainstaluj závislosti:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Spusť aplikaci:
   ```bash
   python main.py
   ```

## Android
- Pro Android je možné použít `buildozer` nebo `p4a`.
- Vygeneruj `buildozer.spec` (nebo použij připravený soubor), nastav `requirements = kivy,plyer`
- Postup pro Linux/WSL:
  ```bash
  buildozer android debug
  ```

## Poznámky
- Desktopové blokování webů funguje úpravou systémového `hosts` souboru, takže je nutné spustit aplikaci jako administrátor / root.
- Android blokování aplikací podle času v plné míře nelze bez systémových oprávnění nebo speciální služby snadno realizovat z čistého Kivy projektu.
- Současná verze poskytuje desktopový blokátor webů v prohlížeči a bezpečný interní browser. Pro Android je potřeba doplnit další native službu nebo VPN/Accessibility řešení.
- Pro Android je třeba mít pro sestavení Linux/WSL prostředí.
