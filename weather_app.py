import glob
import json
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import requests
except ImportError:
    raise ImportError('Please install requests package: pip install requests')

PIL_AVAILABLE = False


WEATHER_CODES = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    77: 'Snow grains',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with hail',
    99: 'Thunderstorm with heavy hail'
}


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Weather App')
        self.geometry('980x720')
        self.configure(bg='#F0F0F0')
        self.resizable(True, True)

        self.data_file = 'weather_app_default.json'
        self.history = []
        self.favorites = []
        self.cache = {}
        self.users = self._get_users()
        self._load_data()

        self.user_zip = tk.StringVar()
        self.unit = tk.StringVar(value='metric')
        self.selected_city = tk.StringVar()
        self.user_var = tk.StringVar(value='default')

        self._build_ui()

        self._refresh_history()
        self._refresh_favorites()

    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self.favorites = data.get('favorites', [])
            except:
                pass

    def _save_data(self):
        data = {
            'history': self.history,
            'favorites': self.favorites
        }
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def _get_api_key(self):
        # No API key needed for free Open-Meteo and Nominatim
        return 'free'

    def _build_ui(self):
        user_frame = ttk.Frame(self, style='Card.TFrame')
        user_frame.pack(fill='x', padx=12, pady=5)

        user_label = ttk.Label(user_frame, text='User:', font=('Segoe UI', 12))
        user_label.grid(row=0, column=0, sticky='w', padx=6, pady=6)

        self.user_combo = ttk.Combobox(user_frame, textvariable=self.user_var, values=self.users, state='readonly', font=('Segoe UI', 11))
        self.user_combo.grid(row=0, column=1, sticky='w', padx=6, pady=6)
        self.user_combo.bind('<<ComboboxSelected>>', lambda e: self._switch_user())

        switch_button = ttk.Button(user_frame, text='New User', command=self._new_user)
        switch_button.grid(row=0, column=2, padx=6, pady=6)

        delete_button = ttk.Button(user_frame, text='Delete User', command=self._delete_user)
        delete_button.grid(row=0, column=3, padx=6, pady=6)

        top_frame = ttk.Frame(self, style='Card.TFrame')
        top_frame.pack(fill='x', padx=12, pady=10)

        city_label = ttk.Label(top_frame, text='City / Location:', font=('Segoe UI', 12))
        city_label.grid(row=0, column=0, sticky='w', padx=6, pady=6)

        city_entry = ttk.Entry(top_frame, width=32, textvariable=self.user_zip, font=('Segoe UI', 11))
        city_entry.grid(row=0, column=1, sticky='w', padx=6, pady=6)
        city_entry.bind('<Return>', lambda e: self._on_search())

        search_button = ttk.Button(top_frame, text='Search', command=self._on_search)
        search_button.grid(row=0, column=2, padx=6, pady=6)

        unit_frame = ttk.Frame(top_frame)
        unit_frame.grid(row=0, column=3, padx=5, pady=6)

        for val, text in [('metric', 'Celsius'), ('imperial', 'Fahrenheit')]:
            r = ttk.Radiobutton(unit_frame, text=text, value=val, variable=self.unit, command=self._on_search)
            r.pack(side='left', padx=3)

        api_help = ttk.Label(top_frame, text='Free worldwide weather data - Powered by Open-Meteo', font=('Segoe UI', 9, 'italic'))
        api_help.grid(row=1, column=0, columnspan=4, sticky='w', padx=6)

        main_frame = ttk.Frame(self, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=12, pady=5)

        self.current_card = tk.Frame(main_frame, bg='white', bd=1, relief='solid')
        self.current_card.pack(fill='x', padx=6, pady=6)

        self.status_label = ttk.Label(self.current_card, text='Enter a city or location and press Search', font=('Segoe UI', 11), background='white', foreground='black')
        self.status_label.pack(pady=18)

        self.details_frame = ttk.Frame(self.current_card)
        self.details_frame.pack(fill='x', padx=12, pady=8)

        self.city_display = ttk.Label(self.details_frame, text='', font=('Segoe UI', 18, 'bold'))
        self.city_display.grid(row=0, column=0, sticky='w', pady=6, columnspan=4)

        self.shadow_icon = ttk.Label(self.details_frame)
        self.shadow_icon.grid(row=1, column=0, rowspan=3, padx=6)

        self.temp_label = ttk.Label(self.details_frame, text='', font=('Segoe UI', 32, 'bold'))
        self.temp_label.grid(row=1, column=1, sticky='w', padx=6)

        self.desc_label = ttk.Label(self.details_frame, text='', font=('Segoe UI', 13))
        self.desc_label.grid(row=2, column=1, sticky='w', padx=6)

        self.extra_label = ttk.Label(self.details_frame, text='', font=('Segoe UI', 11))
        self.extra_label.grid(row=3, column=1, sticky='w', padx=6)

        fav_button = ttk.Button(self.details_frame, text='★ Add to Favorites', command=self._add_favorite)
        fav_button.grid(row=1, column=3, rowspan=2, padx=8, pady=8)

        # Forecast and graph section
        self.forecast_frame = ttk.LabelFrame(main_frame, text='5-day Forecast', padding=10)
        self.forecast_frame.pack(fill='x', padx=6, pady=6)

        self.forecast_panels = []
        for i in range(5):
            panel = ttk.Frame(self.forecast_frame, style='Card.TFrame', borderwidth=1, relief='solid', padding=8)
            panel.grid(row=0, column=i, padx=4, pady=4, sticky='n')
            self.forecast_panels.append(panel)

        # Side bar: history + favorites
        right_frame = ttk.Frame(self, style='Card.TFrame')
        right_frame.pack(fill='both', expand=False, padx=12, pady=6)

        hist_label = ttk.Label(right_frame, text='Search History', font=('Segoe UI', 11, 'bold'))
        hist_label.pack(anchor='w', padx=6, pady=(4, 2))

        self.history_listbox = tk.Listbox(right_frame, height=7, bg='white', fg='black', selectbackground='#A0A0A0')
        self.history_listbox.pack(fill='x', padx=6, pady=2)
        self.history_listbox.bind('<<ListboxSelect>>', self._on_history_select)

        fav_label = ttk.Label(right_frame, text='Favorites', font=('Segoe UI', 11, 'bold'))
        fav_label.pack(anchor='w', padx=6, pady=(8, 2))

        self.favorites_listbox = tk.Listbox(right_frame, height=5, bg='white', fg='black', selectbackground='#A0A0A0')
        self.favorites_listbox.pack(fill='x', padx=6, pady=2)
        self.favorites_listbox.bind('<<ListboxSelect>>', self._on_favorite_select)

        clear_button = ttk.Button(right_frame, text='Clear History', command=self._clear_history)
        clear_button.pack(anchor='center', pady=8)

        self.protocol('WM_DELETE_WINDOW', self._on_close)

        self._apply_style()

    def _get_users(self):
        files = glob.glob('weather_app_*.json')
        users = ['default']
        for f in files:
            user = f.replace('weather_app_', '').replace('.json', '')
            if user not in users:
                users.append(user)
        return sorted(users)

    def _new_user(self):
        new_user = tk.simpledialog.askstring('New User', 'Enter new username:')
        if new_user and new_user.strip():
            username = new_user.strip()
            if username not in self.users:
                self.users.append(username)
                self.users.sort()
                self.user_combo['values'] = self.users
                self.user_var.set(username)
                self._switch_user()
            else:
                messagebox.showinfo('User Exists', 'User already exists.')

    def _delete_user(self):
        username = self.user_var.get()
        if username == 'default':
            messagebox.showwarning('Cannot Delete', 'Cannot delete default user.')
            return
        if messagebox.askyesno('Delete User', f'Delete user "{username}" and all their data?'):
            try:
                os.remove(f'weather_app_{username}.json')
                self.users.remove(username)
                self.user_combo['values'] = self.users
                self.user_var.set('default')
                self._switch_user()
            except:
                pass

    def _switch_user(self):
        username = self.user_var.get().strip()
        if not username:
            username = 'default'
            self.user_var.set(username)
        if username not in self.users:
            self.users.append(username)
            self.users.sort()
            self.user_combo['values'] = self.users
        self.data_file = f'weather_app_{username}.json'
        self.history = []
        self.favorites = []
        self._load_data()
        self._refresh_history()
        self._refresh_favorites()
        # Clear current weather display
        self.city_display.config(text='')
        self.temp_label.config(text='')
        self.desc_label.config(text='')
        self.extra_label.config(text='')
        self.shadow_icon.config(text='')
        for panel in self.forecast_panels:
            for child in panel.winfo_children():
                child.destroy()
        self.status_label.config(text=f'Switched to user: {username}')

    def _on_close(self):
        self._save_data()
        self.destroy()

    def _apply_style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Card.TFrame', background='#E0E0E0')
        style.configure('TLabel', background='#E0E0E0', foreground='black', font=('Segoe UI', 10))
        style.configure('TButton', background='#C0C0C0', foreground='black', font=('Segoe UI', 10))
        style.map('TButton', background=[('active', '#A0A0A0')])
        style.configure('TEntry', fieldbackground='white', foreground='black', insertcolor='black')
        style.configure('TCheckbutton', background='#E0E0E0', foreground='black')
        style.configure('TRadiobutton', background='#E0E0E0', foreground='black')

    def _on_search(self):
        query = self.user_zip.get().strip()
        if not query:
            messagebox.showwarning('Input Required', 'Please enter a city name or location.')
            return

        if query not in self.history:
            self.history.insert(0, query)
            self._refresh_history()
            self._save_data()

        self.selected_city.set(query)
        self.status_label.config(text='Fetching weather ...')

        threading.Thread(target=self._fetch_weather_data, args=(query, self.unit.get()), daemon=True).start()

    def _fetch_weather_data(self, query, unit_mode):
        try:
            if query in self.cache and (time.time() - self.cache[query]['timestamp']) < 900 and self.cache[query]['unit'] == unit_mode:
                data = self.cache[query]['data']
                self._display_weather(data, from_cache=True)
                return

            # Geocode the query using Nominatim
            geocode_url = 'https://nominatim.openstreetmap.org/search'
            geocode_params = {
                'q': query,
                'format': 'json',
                'limit': 1
            }
            geo_r = requests.get(geocode_url, params=geocode_params, timeout=10, headers={'User-Agent': 'WeatherApp/1.0'})
            geo_r.raise_for_status()
            geo_data = geo_r.json()
            if not geo_data:
                self._set_status('Location not found')
                return
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            city_name = geo_data[0].get('name', geo_data[0].get('display_name', query).split(',')[0])

            # Get weather from Open-Meteo
            weather_url = 'https://api.open-meteo.com/v1/forecast'
            temp_unit = 'fahrenheit' if unit_mode == 'imperial' else 'celsius'
            weather_params = {
                'latitude': lat,
                'longitude': lon,
                'current_weather': 'true',
                'daily': 'weathercode,temperature_2m_max,temperature_2m_min',
                'temperature_unit': temp_unit,
                'windspeed_unit': 'ms' if unit_mode == 'metric' else 'mph',
                'timezone': 'auto'
            }
            weather_r = requests.get(weather_url, params=weather_params, timeout=10)
            weather_r.raise_for_status()
            weather_data = weather_r.json()

            data = {'current': weather_data['current_weather'], 'daily': weather_data['daily'], 'city': city_name}
            self.cache[query] = {'data': data, 'timestamp': time.time(), 'unit': unit_mode}

            self._display_weather(data)

        except requests.exceptions.HTTPError as he:
            self._set_status(f'HTTP Error: {he.response.status_code} - {he.response.reason}')
        except requests.exceptions.RequestException as e:
            self._set_status('Network error: ' + str(e))
        except Exception as ex:
            self._set_status('Error: ' + str(ex))

    def _set_status(self, msg):
        self.status_label.config(text=msg)

    def _display_weather(self, data, from_cache=False):
        current = data['current']
        daily = data['daily']
        city_name = data['city']

        self.city_display.config(text=city_name)

        desc = WEATHER_CODES.get(current['weathercode'], 'Unknown')
        temp = current['temperature']
        windspeed = current['windspeed']

        unit = '°C' if self.unit.get() == 'metric' else '°F'
        wind_unit = 'm/s' if self.unit.get() == 'metric' else 'mph'

        self.temp_label.config(text=f'{temp:.1f}{unit}')
        self.desc_label.config(text=desc.capitalize())
        self.extra_label.config(text=f'Wind: {windspeed} {wind_unit}')

        icon_code = str(current['weathercode'])
        self._show_weather_icon(icon_code)

        self.status_label.config(text=('Loaded from cache' if from_cache else 'Weather loaded successfully'))

        self._display_forecast(daily, unit)

    def _show_weather_icon(self, icon_code):
        if not PIL_AVAILABLE:
            self.shadow_icon.config(text=f'Weather: {WEATHER_CODES.get(int(icon_code), "Unknown")}', font=('Segoe UI', 12))
            return

        try:
            # Use a simple emoji or text for icon, since Open-Meteo doesn't have icons
            # For simplicity, use text
            self.shadow_icon.config(text=f'Weather: {WEATHER_CODES.get(int(icon_code), "Unknown")}', font=('Segoe UI', 12))
        except Exception:
            self.shadow_icon.config(text=f'Weather: {WEATHER_CODES.get(int(icon_code), "Unknown")}', font=('Segoe UI', 12))

    def _display_forecast(self, daily, unit):
        times = daily['time']
        codes = daily['weathercode']
        max_temps = daily['temperature_2m_max']
        min_temps = daily['temperature_2m_min']

        for idx in range(min(5, len(times))):
            panel = self.forecast_panels[idx]
            for child in panel.winfo_children():
                child.destroy()

            dt_str = times[idx]
            dt = time.strptime(dt_str, '%Y-%m-%d')
            dt_display = time.strftime('%a %d %b', dt)
            code = codes[idx]
            desc = WEATHER_CODES.get(code, 'Unknown')
            mxt = max_temps[idx]
            mnt = min_temps[idx]

            ttk.Label(panel, text=dt_display, font=('Segoe UI', 10, 'bold')).pack(pady=2)
            ttk.Label(panel, text=desc, font=('Segoe UI', 9)).pack()
            ttk.Label(panel, text=f'Max {mxt:.1f}{unit}').pack()
            ttk.Label(panel, text=f'Min {mnt:.1f}{unit}').pack()

    def _refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history[:20]:
            self.history_listbox.insert(tk.END, item)
        self.update_idletasks()

    def _on_history_select(self, event):
        if not self.history_listbox.curselection():
            return
        index = self.history_listbox.curselection()[0]
        city = self.history_listbox.get(index)
        self.user_zip.set(city)
        self._on_search()

    def _on_favorite_select(self, event):
        if not self.favorites_listbox.curselection():
            return
        index = self.favorites_listbox.curselection()[0]
        city = self.favorites_listbox.get(index)
        self.user_zip.set(city)
        self._on_search()

    def _add_favorite(self):
        city = self.selected_city.get() or self.user_zip.get().strip()
        if not city:
            return
        if city not in self.favorites:
            self.favorites.append(city)
            self._refresh_favorites()
            self._save_data()

    def _refresh_favorites(self):
        self.favorites_listbox.delete(0, tk.END)
        for q in self.favorites:
            self.favorites_listbox.insert(tk.END, q)
        self.update_idletasks()

    def _clear_history(self):
        self.history.clear()
        self._refresh_history()
        self._save_data()


def main():
    app = WeatherApp()
    app.mainloop()


if __name__ == '__main__':
    main()
