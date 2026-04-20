import json
from typing import List, Optional, Any
from abc import ABC, abstractmethod
from functools import wraps
import time
import asyncio

"""
================================================================================
OPAKOVACÍ CVIČENÍ: Python Lekce N01 až N20
Tento skript slouží jako kostra úkolu pro studenty. Prvky označené jako "ÚKOL X" 
vyžadují dopsání chybějícího kódu.

Zaměření cvičení:
OOP, Dunder metody, Abstraktní třídy, Zapouzdření, Type Hinting, Vlastní výjimky, 
Context Managers (with), Dekorátory, List Comprehensions a Asynchronní funkce.
================================================================================
"""

# === Lekce N08: Vlastní výjimky ===
class NedostatekZboziError(Exception):
    """Vyvoláno, když na skladě není dostatek zboží pro odebrání."""
    pass

# === Lekce N17: Dekorátory ===
def zmer_cas(func):
    """
    Dekorátor, který změří a vypíše čas běhu funkce.
    Využívá @wraps pro zachování metadat o původní funkci.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        vysledek = func(*args, **kwargs)
        konec = time.perf_counter()
        print(f"[LOG] Funkce '{func.__name__}' trvala {konec - start:.4f} s.")
        return vysledek
    return wrapper

# === Lekce N19: Abstraktní třídy (ABC) a Polymorfismus ===
class Polozka(ABC):
    @abstractmethod
    def ziskej_popis(self) -> str:
        """Abstraktní metoda - každá položka z ní odvozená musí umět vrátit svůj popis."""
        pass

# === Lekce N11, N12, N13, N14: OOP, Dunder metody, Zapouzdření, Typování ===
class Zbozi(Polozka):
    def __init__(self, nazev: str, cena: float, mnozstvi: int):
        self.nazev = nazev
        self.cena = cena
        self.__mnozstvi = mnozstvi  # Zapouzdření (privátní atribut)

    @property
    def mnozstvi(self) -> int:
        """Getter vracející aktuální množství."""
        return self.__mnozstvi

    def odeber(self, pocet: int) -> None:
        """
        ÚKOL 1: Ošetření skladu (Lekce N05, N08)
        DOPLŇTE KÓD: Pokud je 'pocet' větší než aktuální 'self.__mnozstvi',
        vyhoďte výjimku NedostatekZboziError (s nějakou smysluplnou zprávou). 
        V opačném případě snižte stav o 'pocet'.
        """
        if pocet > self.__mnozstvi:
            raise NedostatekZboziError(f"Na skladě není dostatek zboží '{self.nazev}'.")
        self.__mnozstvi -= pocet

    def ziskej_popis(self) -> str:
        # Přebíjí (implementuje) abstraktní metodu ABC
        return f"Zboží: {self.nazev} ({self.cena} Kč) - Skladem: {self.mnozstvi} ks"

    def __str__(self) -> str:
        """
        ÚKOL 2: Hezký uživatelský výpis (Lekce N10, N13)
        DOPLŇTE KÓD: Vraťte naformátovaný text vlastností pomocí f-stringu.
        Např. "Kniha Python | 600.00 Kč | 10 ks" (Doporučeno zaokrouhlit peníze na 2 desít. místa).
        """
        return f"{self.nazev} | {self.cena:.2f} Kč | {self.mnozstvi} ks"

    def __repr__(self) -> str:
        # Technický výpis (Lekce N13)
        return f"Zbozi(nazev={self.nazev!r}, cena={self.cena!r}, mnozstvi={self.mnozstvi!r})"

# === Lekce N18: Context Managery ===
class ZapisovacDatabaze:
    """Správce kontextu (Context Manager) pro bezpečný zápis událostí do JSON logu."""
    def __init__(self, soubor: str):
        self.soubor = soubor
        self.data: List[dict] = []

    def __enter__(self):
        print(f"[DB] Odbavuji transakci (databáze otevírána).")
        return self

    def pridej_zaznam(self, zaznam: dict):
        self.data.append(zaznam)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        ÚKOL 3: Bezpečný zápis do JSON (Lekce N07, N18)
        DOPLŇTE KÓD:
        - Pokud nedošlo k chybě (tj. exc_type is None), uložte obsah self.data do souboru self.soubor 
          ve formátu JSON (použijte modul json, např. json.dump).
        - Pokud došlo k chybě ve sjednoceném WITH bloku, vypište do konzole nápis, 
          že operace selhala a data byla zničena (odstraněna z cache - nic neukládejte).
        """
        print("[DB] Uzavírám transakci.")
        pass # <--- DOPLŇ ZDE

# === Lekce N15: Generátory, comprehensions (List Comprehension) ===
@zmer_cas
def filtruj_a_zlevni(zbozi_list: List[Zbozi], max_cena: float, sleva_procenta: float) -> List[Zbozi]:
    """
    ÚKOL 4: Kolekce a modifikace (Lekce N03, N15)
    DOPLŇTE KÓD:
    Pomocí list comprehension vyberte pouze to zboží z pole, jehož 'cena' je <= 'max_cena'.
    Těmto konkrétním položkám následně nastavte novou nižší cenu podle procent v 'sleva_procenta'.
    Vraťte upravený seznam produktů ven.
    """
    return [] # <--- DOPLŇ / UPRAV ZDE

# === Lekce N20: Asynchronní programování ===
async def over_dostupnost_api(nazev_produktu: str) -> bool:
    """
    ÚKOL 5: Simulace async požadavku na databázi dodavatele (Lekce N20)
    DOPLŇTE KÓD:
    Spící korutina (simulace sítě) asynchronně uspaná na 1 vteřinu (asyncio.sleep).
    Vraťte 'True' jako simulaci naskladnění existujícího produktu u dodavatelů.
    """
    pass # <--- DOPLŇ ZDE

async def asynchronni_test():
    """Hlavní async loop runner pro ověření dostupnosti na serveru."""
    print("\n--- Start asynchronní prověrky dodavatelů ---")
    task1 = asyncio.create_task(over_dostupnost_api("Kniha Python"))
    task2 = asyncio.create_task(over_dostupnost_api("Klávesnice"))
    
    # Paralelní odbavení
    await asyncio.gather(task1, task2)
    print("--- Asynchronní prověrka dokončena ---")

# === HLAVNÍ BLOK PROGRAMU ===
def main():
    sklad_zbozi = [
        Zbozi("Kniha Python", 600.0, 10),
        Zbozi("Klávesnice", 1200.0, 5),
        Zbozi("Myš", 400.0, 2),
        Zbozi("Monitor", 5000.0, 0)
    ]

    print("=== Původní sklad (Test metod Dunder / repr) ===")
    for z in sklad_zbozi:
        print(repr(z))  # Otestuje magickou metodu __repr__

    print("\n=== Zlevněné dostupné zboží (do 1000 Kč, sleva 20%) ===")
    # Spustí se funkce přes logovací dekorátor
    dostupne_zlevnene = filtruj_a_zlevni(sklad_zbozi, max_cena=1000.0, sleva_procenta=20.0)
    for z in dostupne_zlevnene:
         print(z) # Zde se otestuje __str__ studenta

    print("\n=== Test context manageru s chybou ===")
    try:
        # Zkušební využití vlastního context manageru
        with ZapisovacDatabaze("sklad_export.json") as db:
            db.pridej_zaznam({"akce": "export_zbozi_start", "pocet": len(sklad_zbozi)})
            
            # Simulace chyby (Cílené selhání - odebíráme víc než je povoleno)
            print("Pokouším se odebírat produkt Myš (chci 5 kusů - chyba!)...")
            mys = next(z for z in sklad_zbozi if z.nazev == "Myš")
            mys.odeber(5)  
            
            # Sem kód vůbec nedojde kvůli výjimce!
            db.pridej_zaznam({"akce": "odebrano_uspesne", "pocet": 5})

    except NedostatekZboziError as e:
        print(f"BOMBA! Výjimka úspěšně zachycena programem: {e}")

    # Startovní okruh asynchronních úloh (Lekce N20)
    asyncio.run(asynchronni_test())

if __name__ == "__main__":
    main()
