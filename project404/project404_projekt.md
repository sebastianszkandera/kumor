# Project404

## Popis a cíl projektu
Jednoduchá aplikace pro registraci a přihlášení v Pythonu pomocí `tkinter`. Cílem je ukázat základní práci s uživatelskými údaji a ukládání do souboru.

## Popis funkcionality programu
- Registrace nového uživatele
- Ověření hesla a potvrzení hesla
- Přihlášení existujícího uživatele
- Ukládání přihlašovacích údajů do JSON souboru `names_passwords.json`

## Technická část
- `tkinter` pro grafické rozhraní
- `json` pro ukládání dat
- `os` pro správu cesty k datovému souboru
- Data se ukládají v plném textu, tedy projekt slouží pouze jako vzdělávací ukázka

## Spuštění
```bash
python project404\app_registration_&_login.py
```

## Poznámky
V reálném projektu by hesla nikdy neměla být ukládána v plaintextu. Tento prototyp je pouze pro ukázku logiky registrace a přihlášení.