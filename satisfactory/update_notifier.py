"""
Satisfactory Mod Notifier - Simplified Version
Monitors mod availability and sends notifications when mods become available for Satisfactory 1.2
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("ℹ️ plyer not installed. Install with: pip install plyer")


class ModNotifier:
    def __init__(self):
        self.status_file = Path(__file__).parent / "mod_status.json"
        self.log_file = Path(__file__).parent / "mod_notifier.log"

        # Default mods to track
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
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r') as f:
                    data = json.load(f)
                    self.mods = data.get("mods", self.mods)
            except Exception as e:
                self.log(f"Error loading status: {e}")

    def save_status(self):
        try:
            with open(self.status_file, 'w') as f:
                json.dump({
                    "mods": self.mods,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.log(f"Error saving status: {e}")

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Logging error: {e}")

    def notify(self, title, message):
        if not NOTIFICATIONS_AVAILABLE:
            print(f"🔔 NOTIFICATION: {title}\n   {message}")
            return

        try:
            notification.notify(title=title, message=message, timeout=10)
            self.log(f"Notification sent: {title}")
        except Exception as e:
            self.log(f"Notification error: {e}")

    def mark_available(self, mod_name):
        if mod_name not in self.mods:
            print(f"❌ Mod not found: {mod_name}")
            return

        was_available = self.mods[mod_name]
        self.mods[mod_name] = True
        self.save_status()

        if not was_available:
            print(f"✅ {mod_name} marked as available for Satisfactory 1.2")
            self.notify("✅ Mod Available for Satisfactory 1.2", mod_name)
        else:
            print(f"ℹ️ {mod_name} was already marked as available")

    def mark_unavailable(self, mod_name):
        if mod_name not in self.mods:
            print(f"❌ Mod not found: {mod_name}")
            return

        self.mods[mod_name] = False
        self.save_status()
        print(f"⏳ {mod_name} marked as unavailable")

    def show_status(self):
        print("\n📋 Mod Status for Satisfactory 1.2:")
        print("=" * 50)

        available = [name for name, status in self.mods.items() if status]
        unavailable = [name for name, status in self.mods.items() if not status]

        if available:
            print(f"\n✅ Available ({len(available)}):")
            for mod in available:
                print(f"   - {mod}")

        if unavailable:
            print(f"\n⏳ Not yet available ({len(unavailable)}):")
            for mod in unavailable:
                print(f"   - {mod}")

        print("=" * 50 + "\n")

    def add_mod(self, mod_name):
        if mod_name in self.mods:
            print(f"ℹ️ {mod_name} is already being tracked")
            return

        self.mods[mod_name] = False
        self.save_status()
        print(f"✅ {mod_name} added to tracking list")

    def remove_mod(self, mod_name):
        if mod_name not in self.mods:
            print(f"❌ Mod not found: {mod_name}")
            return

        del self.mods[mod_name]
        self.save_status()
        print(f"✅ {mod_name} removed from tracking")


def main():
    notifier = ModNotifier()

    print("\n🎮 Satisfactory Mod Notifier for v1.2\n")

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "status":
            notifier.show_status()
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
            print("Testing notifications...")
            notifier.notify("🧪 Test Notification", "If you see this, notifications are working!")
            print("✅ Notification sent! Check your screen.")
        else:
            print("Usage:")
            print("  python update_notifier.py status                    - Show all mod statuses")
            print("  python update_notifier.py available <mod_name>      - Mark mod as available (sends notification)")
            print("  python update_notifier.py unavailable <mod_name>    - Mark mod as unavailable")
            print("  python update_notifier.py add <mod_name>            - Add mod to tracking")
            print("  python update_notifier.py remove <mod_name>         - Remove mod from tracking")
            print("  python update_notifier.py test                      - Test notifications")
    else:
        notifier.show_status()


if __name__ == "__main__":
    main()
