# Upozorňovač dostupnosti módů Satisfactory

🎮 Monitoruje módy na **ficsit.app** a odesílá **oznamovací zprávy pultu Windows** když jsou k dispozici pro **Satisfactory 1.2**.

## Funkce

✅ Monitoruje populární módy Satisfactory  
✅ Kontroluje dostupnost pro verzi 1.2  
✅ Oznamovací zprávy pultu Windows  
✅ Přizpůsobitelný seznam módů  
✅ Jednorázové kontroly nebo nepřetržité monitorování  
✅ Protokolování pro sledování všech kontrol  

## Nastavení

### 1. Instalace závislostí

Otevřete PowerShell v této složce a spusťte:

```powershell
pip install -r requirements.txt
```

Nebo ručně nainstalujte:
```powershell
pip install requests win10toast
```

### 2. Spuštění skriptu

**Jednorazová kontrola módů:**
```powershell
python update_notifier.py status
```

**Označení módu jako dostupného (odesílá oznamovací zprávu):**
```powershell
python update_notifier.py available "Název módu"
```

**Označení módu jako nedostupného:**
```powershell
python update_notifier.py unavailable "Název módu"
```

**Přidání nového módu k monitorování:**
```powershell
python update_notifier.py add "Název módu"
```

**Odebrání módu z monitorování:**
```powershell
python update_notifier.py remove "Název módu"
```

**Test oznamovacích zpráv:**
```powershell
python update_notifier.py test
```

## Konfigurація

### Výchozí monitorované módy

Skript monitoruje tyto módy ve výchozím nastavení:
- Refined Power
- Satisfactory Mod Loader
- Infinite Zoop
- Infinite Nudge
- MK++
- Content Lib

### Přizpůsobení módů

Upravte `mod_status.json` pro změnu monitorovaných módů:

```json
{
  "mods": {
    "Refined Power": false,
    "Váš vlastní mód": false
  }
}
```

## Generované soubory

- `mod_status.json` - Váš seznam módů k monitorování a jejich stav
- `mod_notifier.log` - Úplný protokol všech akcí a notifikací

## Řešení problémů

**Oznamovací zprávy se nezobrazují?**
- Zkontrolujte, zda jsou oznamovací zprávy Windows povoleny v Nastavení
- Zkontrolujte, zda je `plyer` nainstalován: `pip install plyer`

**Mód nenalezen?**
- Ujistěte se, že je mód ve výchozím seznamu
- Zkuste přidat mód pomocí: `python update_notifier.py add "Název módu"`
- Kontrolujte `mod_notifier.log` pro chybové zprávy

## Poznámky

- Skript používá lokální systém sledování
- Vy sami označíte, když se mód stane dostupným
- Oznamovací zprávy se zobrazují po dobu ~10 sekund
- Stav je uložen v `mod_status.json`
- Pro resetování stavu odstraňte nebo upravte `mod_status.json`
