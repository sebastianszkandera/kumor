"""
Upozorňovač dostupnosti módů Satisfactory - Zjednodušená verze
Sleduje dostupnost módů lokálně a odesílá notifikace když se módy stanou dostupnými
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict
import sys

# Pokus importovat plyer pro oznámení na všech platformách
try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("ℹ️ plyer není instalován. Nainstalujte pomocí: pip install plyer")


class ModNotifier:
    """Zjednodušený sledovač módů, který notifikuje když se módy stanou dostupné pro verzi 1.2"""
    
    def __init__(self):
        self.workspace_dir = Path(__file__).parent
        self.status_file = self.workspace_dir / "mod_status.json"
        self.log_file = self.workspace_dir / "mod_notifier.log"
        
        # Výchozí sledované módy
        self.mods = {
            "Refined Power": False,
            "Satisfactory Mod Loader": False,
            "Infinite Zoop": False,
            "Infinite Nudge": False,
            "MK++": False,
            "Content Lib": False,
        }
        
        self.load_status()
    
    def load_status(self):
        """Načti aktuální stav módů ze souboru"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r') as f:
                    data = json.load(f)
                    self.mods = data.get("mods", self.mods)
                    self.log(f"Stav módů načten ze souboru")
            except Exception as e:
                self.log(f"Chyba při načítání stavového souboru: {e}", level="WARNING")
        else:
            self.save_status()
    
    def save_status(self):
        """Ulož aktuální stav módů do souboru"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump({
                    "mods": self.mods,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.log(f"Chyba při ukládání stavu: {e}", level="ERROR")
    
    def log(self, message: str, level: str = "INFO"):
        """Zaloguj zprávy do souboru a konzole"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        print(log_message)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Chyba při zápisu do logu: {e}")
    
    def notify(self, title: str, message: str):
        """Pošli notifikaci na pultu"""
        if not NOTIFICATIONS_AVAILABLE:
            print(f"🔔 NOTIFIKACE: {title}\n   {message}")
            return
        
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
            self.log(f"Notifikace odeslána: {title}")
        except Exception as e:
            self.log(f"Chyba při odesílání notifikace: {e}", level="ERROR")
    
    def mark_available(self, mod_name: str):
        """Označ mód jako dostupný a pošli notifikaci"""
        if mod_name not in self.mods:
            print(f"❌ Mód nenalezen: {mod_name}")
            print(f"Dostupné módy: {', '.join(self.mods.keys())}")
            return
        
        was_available = self.mods[mod_name]
        self.mods[mod_name] = True
        self.save_status()
        
        if not was_available:
            print(f"✅ Mód {mod_name} označen jako dostupný pro Satisfactory 1.2")
            self.log(f"{mod_name} označen jako dostupný")
            
            # Pošli notifikaci
            self.notify(
                title="✅ Mód dostupný pro Satisfactory 1.2",
                message=mod_name
            )
        else:
            print(f"ℹ️ {mod_name} byl již označen jako dostupný")
    
    def mark_unavailable(self, mod_name: str):
        """Označ mód jako nedostupný"""
        if mod_name not in self.mods:
            print(f"❌ Mód nenalezen: {mod_name}")
            return
        
        self.mods[mod_name] = False
        self.save_status()
        print(f"⏳ Mód {mod_name} označen jako nedostupný")
        self.log(f"{mod_name} označen jako nedostupný")
    
    def check_status(self):
        """Zobraz aktuální stav všech módů"""
        print("\n📋 Stav módů pro Satisfactory 1.2:")
        print("=" * 50)
        
        available = [name for name, status in self.mods.items() if status]
        unavailable = [name for name, status in self.mods.items() if not status]
        
        if available:
            print(f"\n✅ Dostupné ({len(available)}):")
            for mod in available:
                print(f"   - {mod}")
        
        if unavailable:
            print(f"\n⏳ Dosud nedostupné ({len(unavailable)}):")
            for mod in unavailable:
                print(f"   - {mod}")
        
        print("=" * 50 + "\n")
    
    def add_mod(self, mod_name: str):
        """Přidej nový mód k sledování"""
        if mod_name in self.mods:
            print(f"ℹ️ Mód {mod_name} je již sledován")
            return
        
        self.mods[mod_name] = False
        self.save_status()
        print(f"✅ Mód {mod_name} přidán do seznamu sledování")
    
    def remove_mod(self, mod_name: str):
        """Odebři mód ze sledování"""
        if mod_name not in self.mods:
            print(f"❌ Mód nenalezen: {mod_name}")
            return
        
        del self.mods[mod_name]
        self.save_status()
        print(f"✅ Mód {mod_name} odebrán ze sledování")


def main():
    """Hlavní vstupní bod"""
    notifier = ModNotifier()
    
    print("\n🎮 Upozorňovač dostupnosti módů Satisfactory pro v1.2\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            notifier.check_status()
        elif command == "available" and len(sys.argv) > 2:
            mod_name = " ".join(sys.argv[2:])
            notifier.mark_available(mod_name)
        elif command == "unavailable" and len(sys.argv) > 2:
            mod_name = " ".join(sys.argv[2:])
            notifier.mark_unavailable(mod_name)
        elif command == "add" and len(sys.argv) > 2:
            mod_name = " ".join(sys.argv[2:])
            notifier.add_mod(mod_name)
        elif command == "remove" and len(sys.argv) > 2:
            mod_name = " ".join(sys.argv[2:])
            notifier.remove_mod(mod_name)
        elif command == "test":
            print("Testování notifikací na pultu...")
            notifier.notify("🧪 Testovací notifikace", "Pokud vidíte tuto zprávu, notifikace fungují!")
            print("✅ Notifikace odeslána! Zkontrolujte svou obrazovku.")
        else:
            print("Použití:")
            print("  python update_notifier.py status                    - Zobraz stavy všech módů")
            print("  python update_notifier.py available <název_módu>    - Označ mód jako dostupný (odesílá notifikaci)")
            print("  python update_notifier.py unavailable <název_módu>  - Označ mód jako nedostupný")
            print("  python update_notifier.py add <název_módu>          - Přidej mód k sledování")
            print("  python update_notifier.py remove <název_módu>       - Odebři mód ze sledování")
            print("  python update_notifier.py test                      - Testuj notifikace")
            print()
            print("Příklady:")
            print("  python update_notifier.py available \"Refined Power\"")
            print("  python update_notifier.py status")
            print()
    else:
        # Výchozí: zobraz stav
        notifier.check_status()


if __name__ == "__main__":
    main()
