# Project3

## Popis a cíl projektu
Mobilní aplikace pro výpočet, zda se vyplatí koupit položku podle hodinové sazby a osobního názoru. Cílem je ukázat uživatelské rozhraní připravené pro mobilní i desktopové použití.

## Popis funkcionality programu
- Kalkulačka položky hodnoty vzhledem k hodinové mzdě
- Možnost přidat fotografii položky
- Historie uložených položek
- Ukládání dat do `worth_it_data.json`
- Pokusy o podporu mobilního exportu pomocí Kivy a Buildozer

## Technická část
- `Kivy` pro mobilní UI
- `python` pro hlavní logiku
- Možnost exportu na Android pomocí Buildozer
- Data se ukládají do JSON souboru

## Spuštění
```bash
pip install -r project3\requirements.txt
python project3\project3.py
```

## Poznámky
Projekt obsahuje mobilní přístup a desktopovou verzi. Pokud chcete vytvořit APK, použijte Buildozer nebo Kivy Toolchain.