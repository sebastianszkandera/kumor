from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
import json
import os
import math
from datetime import datetime

# Set window size for better mobile preview
Window.size = (400, 800)

class WorthItApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "worth_it_data.json"
        self.hourly_rate = 15.0
        self.load_data()
    
    def load_data(self):
        """Load stored data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.hourly_rate = data.get("hourly_rate", 15.0)
                self.items_history = data.get("items", [])
        else:
            self.items_history = []
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            "hourly_rate": self.hourly_rate,
            "items": self.items_history
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def format_hours(self, hours_needed):
        """Convert hours to days and hours format"""
        if hours_needed < 24:
            hour_text = "hour" if hours_needed == 1 else "hours"
            return f"{hours_needed} {hour_text}"
        else:
            days = hours_needed // 24
            remaining_hours = hours_needed % 24
            
            days_text = "day" if days == 1 else "days"
            
            if remaining_hours == 0:
                return f"{days} {days_text}"
            else:
                hour_text = "hour" if remaining_hours == 1 else "hours"
                return f"{days} {days_text} and {remaining_hours} {hour_text}"
    
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tab selector
        tab_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        calc_btn = Button(text="Calculator", size_hint_x=0.5)
        calc_btn.bind(on_press=self.show_calculator)
        history_btn = Button(text="History", size_hint_x=0.5)
        history_btn.bind(on_press=self.show_history)
        tab_layout.add_widget(calc_btn)
        tab_layout.add_widget(history_btn)
        
        self.main_layout.add_widget(tab_layout)
        
        # Container for switching screens
        self.screen_container = BoxLayout()
        self.main_layout.add_widget(self.screen_container)
        
        self.show_calculator()
        return self.main_layout
    
    def show_calculator(self, *args):
        """Show calculator screen"""
        self.screen_container.clear_widgets()
        calc_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Hourly Rate
        calc_layout.add_widget(Label(text="Hourly Rate ($):", size_hint_y=0.1))
        self.rate_input = TextInput(text=str(self.hourly_rate), multiline=False, size_hint_y=0.1)
        calc_layout.add_widget(self.rate_input)
        
        # Item Name
        calc_layout.add_widget(Label(text="Item Name:", size_hint_y=0.1))
        self.name_input = TextInput(hint_text="Enter item name", multiline=False, size_hint_y=0.1)
        calc_layout.add_widget(self.name_input)
        
        # Item Price
        calc_layout.add_widget(Label(text="Item Price ($):", size_hint_y=0.1))
        self.price_input = TextInput(hint_text="Enter price", multiline=False, size_hint_y=0.1)
        calc_layout.add_widget(self.price_input)
        
        # Opinion
        calc_layout.add_widget(Label(text="Your Opinion:", size_hint_y=0.1))
        self.opinion_input = TextInput(hint_text="Why do you want it?", multiline=True, size_hint_y=0.15)
        calc_layout.add_widget(self.opinion_input)
        
        # Photo Button
        photo_btn = Button(text="Add Photo", size_hint_y=0.1)
        photo_btn.bind(on_press=self.select_photo)
        calc_layout.add_widget(photo_btn)
        
        self.photo_label = Label(text="No photo selected", size_hint_y=0.1)
        calc_layout.add_widget(self.photo_label)
        self.selected_photo = None
        
        # Calculate Button
        calc_btn = Button(text="Calculate Worth", size_hint_y=0.1)
        calc_btn.bind(on_press=self.calculate)
        calc_layout.add_widget(calc_btn)
        
        # Result
        self.result_label = Label(text="", size_hint_y=0.2)
        calc_layout.add_widget(self.result_label)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(calc_layout)
        self.screen_container.add_widget(scroll)
    
    def select_photo(self, *args):
        """Open file chooser for photo selection"""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        def select_file(path, filename):
            if filename:
                self.selected_photo = os.path.join(path, filename[0])
                self.photo_label.text = f"Photo: {filename[0][:20]}..."
                popup.dismiss()
        
        select_btn = Button(text='Select')
        select_btn.bind(on_press=lambda x: select_file(filechooser.path, filechooser.selection))
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='Select Photo', content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def calculate(self, *args):
        """Calculate hours needed and save item"""
        try:
            hourly_rate = float(self.rate_input.text)
            price = float(self.price_input.text)
            name = self.name_input.text or "Unnamed Item"
            opinion = self.opinion_input.text or "No opinion"
            
            self.hourly_rate = hourly_rate
            
            hours_needed = math.ceil(price / hourly_rate)
            time_format = self.format_hours(hours_needed)
            
            result_text = f"You need to work {time_format}\nto afford {name}!"
            self.result_label.text = result_text
            
            # Save to history
            item = {
                "name": name,
                "price": price,
                "hourly_rate": hourly_rate,
                "hours_needed": hours_needed,
                "opinion": opinion,
                "photo": self.selected_photo,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.items_history.append(item)
            self.save_data()
            
            # Show save confirmation
            from kivy.uix.popup import Popup
            popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_layout.add_widget(Label(text=f"✓ {name} saved to history!"))
            close_btn = Button(text='Close', size_hint_y=0.3)
            popup_layout.add_widget(close_btn)
            popup = Popup(title='Saved', content=popup_layout, size_hint=(0.8, 0.3))
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            
        except ValueError:
            from kivy.uix.popup import Popup
            popup_layout = BoxLayout(orientation='vertical', padding=10)
            popup_layout.add_widget(Label(text="Please enter valid numbers!"))
            close_btn = Button(text='Close', size_hint_y=0.3)
            popup_layout.add_widget(close_btn)
            popup = Popup(title='Error', content=popup_layout, size_hint=(0.8, 0.3))
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
    
    def show_history(self, *args):
        """Show history of items"""
        self.screen_container.clear_widgets()
        history_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        if not self.items_history:
            history_layout.add_widget(Label(text="No items in history yet!", size_hint_y=1))
        else:
            scroll = ScrollView()
            items_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
            items_grid.bind(minimum_height=items_grid.setter('height'))
            
            for item in reversed(self.items_history):
                item_box = self.create_item_card(item)
                items_grid.add_widget(item_box)
            
            scroll.add_widget(items_grid)
            history_layout.add_widget(scroll)
        
        # Clear history button
        clear_btn = Button(text="Clear History", size_hint_y=0.1)
        clear_btn.bind(on_press=self.clear_history)
        history_layout.add_widget(clear_btn)
        
        self.screen_container.add_widget(history_layout)
    
    def create_item_card(self, item):
        """Create a card widget for displaying item"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=5, padding=10)
        card.canvas.clear()
        
        card.add_widget(Label(text=f"📦 {item['name']}", size_hint_y=0.2, bold=True))
        card.add_widget(Label(text=f"Price: ${item['price']}", size_hint_y=0.15))
        time_format = self.format_hours(item['hours_needed'])
        card.add_widget(Label(text=f"Time needed: {time_format}", size_hint_y=0.15))
        card.add_widget(Label(text=f"💭 {item['opinion'][:50]}...", size_hint_y=0.2))
        card.add_widget(Label(text=f"📅 {item['date']}", size_hint_y=0.15))
        
        return card
    
    def clear_history(self, *args):
        """Clear all history"""
        self.items_history = []
        self.save_data()
        self.show_history()

if __name__ == '__main__':
    WorthItApp().run()