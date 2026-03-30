# Satisfactory Mod Notifier

🎮 Monitors mods on ficsit.app and sends desktop notifications when they become available for **Satisfactory 1.2**.

## Features

✅ Monitors popular Satisfactory mods
✅ Checks availability for version 1.2
✅ Desktop notifications
✅ Customizable mod list
✅ Command-line interface

## Setup

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

Or manually:
```powershell
pip install plyer
```

### 2. Run the Script

**Show mod statuses:**
```powershell
python update_notifier.py status
```

**Mark mod as available (sends notification):**
```powershell
python update_notifier.py available "Mod Name"
```

**Mark mod as unavailable:**
```powershell
python update_notifier.py unavailable "Mod Name"
```

**Add new mod to track:**
```powershell
python update_notifier.py add "Mod Name"
```

**Remove mod from tracking:**
```powershell
python update_notifier.py remove "Mod Name"
```

**Test notifications:**
```powershell
python update_notifier.py test
```

## Default Tracked Mods

- Refined Power
- Satisfactory Mod Loader
- Infinite Zoop
- Infinite Nudge
- MK++
- Content Lib

## Files

- `mod_status.json` - Your mod tracking list and statuses
- `mod_notifier.log` - Activity log

## Troubleshooting

**Notifications not showing?**
- Ensure Windows notifications are enabled in Settings
- Install plyer: `pip install plyer`

## Poznámky

- Skript používá lokální systém sledování
- Vy sami označíte, když se mód stane dostupným
- Oznamovací zprávy se zobrazují po dobu ~10 sekund
- Stav je uložen v `mod_status.json`
- Pro resetování stavu odstraňte nebo upravte `mod_status.json`
