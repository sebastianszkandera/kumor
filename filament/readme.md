Filament Cost Counter

Tento program slouží k výpočtu nákladů na 3D tisk filamentu včetně ceny materiálu, elektřiny, údržby a amortizace tiskárny.

Popis

Program vytvoří grafické uživatelské rozhraní pomocí knihovny Tkinter, kde můžete zadat různé parametry související s 3D tiskem a získat přesný výpočet celkových nákladů na jeden tisk. Cena filamentu se počítá v EUR (podle cen Bambu Lab store) a převádí se na CZK pomocí aktuálního kurzu.

Požadavky

-Python 3.x
-Knihovny:
  -tkinter (součást standardní distribuce Pythonu)
  -forex-python (pro převod měn)

Instalace

Nejprve nainstalujte potřebnou knihovnu:

```
pip install forex-python
```

Spuštění

Spusťte program příkazem:

```
python filament_cost_counter.py
```

Použití

Po spuštění se otevře okno s následujícími poli pro zadání:

-Filament weight (g): Hmotnost použitého filamentu v gramech
-Cost per kg (EUR): Cena filamentu za kilogram v EUR (výchozí hodnota 11.5 pro Bambu Lab)
-Print time (hours): Čas tisku v hodinách
-Printer power (W): Příkon tiskárny ve wattech (výchozí 120 W)
-Printer usage (%): Procento využití tiskárny během tisku (výchozí 100%)
-Electricity cost (per kWh) in CZK: Cena elektřiny za kWh v CZK (výchozí 6.00)
-Maintenance (CZK per hour): Náklady na údržbu za hodinu v CZK (výchozí 2.00)
-Per-print maintenance (CZK): Jednorázové náklady na údržbu za tisk v CZK (výchozí 0.00)
-Printer purchase price (CZK, optional): Pořizovací cena tiskárny v CZK (volitelné pro amortizaci)
-Printer lifetime hours (optional): Očekávaná životnost tiskárny v hodinách (volitelné pro amortizaci)

Klikněte na tlačítko "Calculate" pro výpočet nákladů.

Výstup

Program zobrazí detailní rozpis nákladů:

-Filament: Cena filamentu v EUR a převedená na CZK
-Electricity: Náklady na elektřinu v CZK (včetně spotřeby v kWh)
-Maintenance: Náklady na údržbu v CZK (hodinová + jednorázová)
-Amortization: Amortizace tiskárny v CZK (pokud jsou zadány volitelné parametry)
-Total: Celkové náklady v CZK

Poznámky

Program vyžaduje připojení k internetu pro získání aktuálního kurzu EUR/CZK
Všechny výpočty jsou v reálném čase pomocí aktuálních kurzů
Amortizace se počítá pouze pokud jsou zadány oba volitelné parametry (cena tiskárny a životnost)

Příklad použití

Pro tisk o hmotnosti 50g filamentu za 11.5 EUR/kg, čas 2 hodiny, tiskárna 120W, elektřina 6 CZK/kWh, údržba 2 CZK/hod:

Celkové náklady budou zahrnovat:
-Filament: ~0.58 EUR (~14.50 CZK)
-Elektřina: ~1.44 CZK
-Údržba: 4.00 CZK
-Celkem: ~19.94 CZK</content>