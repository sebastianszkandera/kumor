# Guitar App

## Popis a cíl projektu
Aplikace rozpoznává kytarové akordy v reálném čase pomocí zvukové analýzy. Cílem je ukázat zpracování zvuku a porovnání s šablonami akordů.

## Popis funkcionality programu
- Nahrávání zvuku z mikrofonu
- Výpočet spektrogramu a chromagramu
- Porovnání aktuálního zvuku s šablonami akordů
- Zobrazení rozpoznaného akordu v reálném čase
- Vyhlazování výsledků pro zvýšení stability výstupu

## Technická část
- `sounddevice` pro zachytávání zvuku
- `librosa` pro analýzu zvuku a výpočet chromatogramu
- `numpy` pro numerické operace
- Detekce používá porovnání kosinové podobnosti mezi chromatogramem a šablonami

## Spuštění
```bash
pip install sounddevice numpy librosa
python guitar\guitar_app.py
```

## Poznámky
Aplikace požaduje funkční mikrofon. Pro stabilní detekci je vhodné čisté zvukové prostředí a jednoduché akordy bez šumu.