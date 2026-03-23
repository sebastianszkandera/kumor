# Dokumentace pro Guitar App

## Popis aplikace

Tato aplikace je nástroj pro rozpoznávání kytarových akordů v reálném čase. Používá mikrofon k záznamu zvuku, analyzuje ho pomocí knihovny Librosa a porovnává s předdefinovanými šablonami akordů. Aplikace rozpoznává více než 30 různých akordů včetně dur, moll, sedmiček a dalších variant.

## Hlavní funkce

- **Rozpoznávání akordů**: Analyzuje zvuk z mikrofonu a identifikuje hraný akord.
- **Knihovna akordů**: Obsahuje šablony pro 30+ akordů (dur, moll, 7, maj7, m7, sus4, add9, atd.).
- **Vyhlazování výsledků**: Používá historii posledních detekcí pro potlačení chyb a stabilizaci výstupu.
- **Reálný čas**: Kontinuálně nahrává a analyzuje zvuk po krátkých intervalech.
- **Prahová hodnota**: Zobrazuje pouze akordy s vysokou shodou (nad 65 %).

## Jak spustit aplikaci

1. Ujistěte se, že máte nainstalovaný Python (verze 3.6 nebo vyšší).
2. Nainstalujte potřebné závislosti:
   ```
   pip install sounddevice numpy librosa
   ```
   (Na Windows/Linux může být potřeba také PortAudio pro sounddevice.)
3. Spusťte aplikaci:
   ```
   python guitar_app.py
   ```
4. Zahrajte akord na kytaru a sledujte výstup v konzoli.

## Závislosti

- **sounddevice**: Pro nahrávání zvuku z mikrofonu.
- **numpy**: Pro matematické operace s poli.
- **librosa**: Pro analýzu zvuku a výpočet chromatogramu.

## Technické detaily

- **Vzorkovací frekvence**: 22050 Hz
- **Délka záznamu**: 0.8 sekundy
- **Vyhlazování**: Okno o velikosti 2 (poslední 2 detekce musí být stejné)
- **Metoda analýzy**: Chromagram (CQT) s 12 chromatickými tóny
- **Porovnání**: Kosinová podobnost mezi chromatogramem a šablonami akordů

## Struktura kódu

- **CHORD_TEMPLATES**: Slovník s binárními šablonami akordů (1 = tón přítomen, 0 = chybí).
- **identify_chord()**: Funkce pro analýzu zvuku a nalezení nejlepší shody.
- **Hlavní smyčka**: Nekonečná smyčka pro kontinuální nahrávání a analýzu.

## Poznámky

- Aplikace vyžaduje funkční mikrofon.
- Pro nejlepší výsledky použijte čistý zvuk kytary bez šumu.
- Aplikace běží v konzoli a vypisuje detekované akordy.
- Ukončete aplikaci pomocí Ctrl+C.

## Autor

Tato aplikace byla vytvořena jako ukázkový projekt pro demonstraci zpracování zvuku a rozpoznávání hudebních akordů v Pythonu.