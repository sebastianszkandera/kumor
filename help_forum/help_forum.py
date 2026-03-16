import tkinter as tk
from tkinter import messagebox
import json
import os

# Třída pro aplikaci fóra
class ForumApp:
    # Inicializace aplikace
    def __init__(self, root):
        self.root = root
        self.root.title("Fórum")
        # Seznam otázek, každá je slovník s otázkou a seznamem odpovědí
        self.questions = []
        # Název souboru pro uložení dat
        self.data_file = "forum_data.json"

        # Vytvoření widgetů
        # Listbox pro zobrazení otázek
        self.question_list = tk.Listbox(root, width=50)
        self.question_list.pack(side=tk.LEFT, fill=tk.Y)
        # Vazba na událost výběru otázky
        self.question_list.bind('<<ListboxSelect>>', self.on_select)

        # Textové pole pro zobrazení odpovědí
        self.reply_text = tk.Text(root, wrap=tk.WORD)
        self.reply_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Vstupní pole pro zadávání otázek nebo odpovědí
        self.entry = tk.Entry(root)
        self.entry.pack(side=tk.BOTTOM, fill=tk.X)

        # Tlačítko pro přidání otázky
        self.add_q_btn = tk.Button(root, text="Přidat otázku", command=self.add_question)
        self.add_q_btn.pack(side=tk.BOTTOM)

        # Tlačítko pro přidání odpovědi
        self.add_r_btn = tk.Button(root, text="Přidat odpověď", command=self.add_reply)
        self.add_r_btn.pack(side=tk.BOTTOM)

        # Načtení dat ze souboru
        self.load_data()

    # Metoda pro načtení dat ze souboru
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.questions = json.load(f)
                # Naplnění listboxu otázkami
                for q in self.questions:
                    self.question_list.insert(tk.END, q['question'])
            except json.JSONDecodeError:
                # Pokud je soubor poškozený, začneme s prázdným seznamem
                self.questions = []

    # Metoda pro uložení dat do souboru
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.questions, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při ukládání dat: {e}")

    # Metoda pro přidání nové otázky
    def add_question(self):
        # Získání textu z vstupního pole
        q = self.entry.get().strip()
        if q:
            # Přidání otázky do seznamu
            self.questions.append({'question': q, 'replies': []})
            # Přidání do listboxu
            self.question_list.insert(tk.END, q)
            # Vymazání vstupního pole
            self.entry.delete(0, tk.END)
            # Uložení dat
            self.save_data()
        else:
            # Zobrazení chybové zprávy, pokud je vstup prázdný
            messagebox.showerror("Chyba", "Otázka nemůže být prázdná!")

    # Metoda pro přidání odpovědi k vybrané otázce
    def add_reply(self):
        # Získání textu z vstupního pole
        r = self.entry.get().strip()
        if r and self.question_list.curselection():
            # Získání indexu vybrané otázky
            idx = self.question_list.curselection()[0]
            # Přidání odpovědi k otázce
            self.questions[idx]['replies'].append(r)
            # Vymazání vstupního pole
            self.entry.delete(0, tk.END)
            # Aktualizace zobrazení odpovědí
            self.on_select(None)
            # Uložení dat
            self.save_data()
        elif not r:
            # Chyba, pokud je odpověď prázdná
            messagebox.showerror("Chyba", "Odpověď nemůže být prázdná!")
        else:
            # Chyba, pokud není vybrána žádná otázka
            messagebox.showerror("Chyba", "Vyberte otázku pro odpověď!")

    # Metoda pro zobrazení odpovědí při výběru otázky
    def on_select(self, event):
        if self.question_list.curselection():
            # Získání indexu vybrané otázky
            idx = self.question_list.curselection()[0]
            q = self.questions[idx]
            # Vymazání textového pole
            self.reply_text.delete(1.0, tk.END)
            # Zobrazení otázky a odpovědí
            self.reply_text.insert(tk.END, f"Otázka: {q['question']}\n\nOdpovědi:\n")
            if q['replies']:
                for r in q['replies']:
                    self.reply_text.insert(tk.END, f"- {r}\n")
            else:
                self.reply_text.insert(tk.END, "Žádné odpovědi zatím.\n")

# Spuštění aplikace
if __name__ == "__main__":
    root = tk.Tk()
    app = ForumApp(root)
    root.mainloop()
