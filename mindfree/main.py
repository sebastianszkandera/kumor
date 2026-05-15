from pathlib import Path
from datetime import datetime
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import re
import ssl
import os
import sys
import ctypes

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class BaseScreen(Screen):
    @property
    def app(self):
        from kivy.app import App
        return App.get_running_app()


class HomeScreen(BaseScreen):
    pass


class BrowserScreen(BaseScreen):
    pass


class MindFreeApp(App):
    current_time = StringProperty('00:00:00')
    daily_usage_label = StringProperty('0 min')
    session_status = StringProperty('Inactive')
    mode_label = StringProperty('Standard')
    progress_label = StringProperty('0 %')
    recommended_text = StringProperty('Use the focus browser and keep your attention on what matters.')
    block_trackers = BooleanProperty(True)
    block_scroll = BooleanProperty(True)
    limit_recommendations = BooleanProperty(True)
    mute_notifications = BooleanProperty(False)
    child_mode = BooleanProperty(False)
    focus_mode = BooleanProperty(False)
    daily_target = NumericProperty(120)
    total_minutes = NumericProperty(0)
    session_seconds = NumericProperty(0)
    current_url = StringProperty('https://www.tiktok.com')
    browser_content = StringProperty('MindFree browser je připravený. Otevři stránku z adresního řádku nebo použij tlačítka.')
    status_message = StringProperty('Ready')
    block_start = StringProperty('22:00')
    block_end = StringProperty('06:00')
    block_status = StringProperty('Block schedule inactive')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = Path(self.user_data_dir) / 'mindfree_data.json'
        self.load_data()

    def build(self):
        self.title = 'MindFree'
        self.icon = 'icon.png' if Path('icon.png').exists() else None
        self.update_status_labels()
        Clock.schedule_interval(self.tick, 1)
        Clock.schedule_interval(self.enforce_browser_block, 30)
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name='home'))
        manager.add_widget(BrowserScreen(name='browser'))
        return manager

    def on_start(self):
        self.notify('MindFree je připravený', 'Použij integrovaný browser a omez zbytečné prvky.')

    def tick(self, dt):
        self.current_time = datetime.now().strftime('%H:%M:%S')
        if self.focus_mode:
            self.session_seconds += dt
            if self.session_seconds >= 60:
                self.total_minutes += 1
                self.session_seconds -= 60
                self.save_data()
                self.update_status_labels()

    def update_status_labels(self):
        self.daily_usage_label = f'{int(self.total_minutes)} min'
        self.session_status = 'Focus active' if self.focus_mode else 'Inactive'
        self.mode_label = 'Child mode' if self.child_mode else 'Standard'
        progress = min(100, int(self.total_minutes / self.daily_target * 100)) if self.daily_target else 0
        self.progress_label = f'{progress} %'
        self.recommended_text = self.build_recommended_text()

    def build_recommended_text(self):
        if self.child_mode:
            return 'Dětský režim: zjednodušený obsah a méně nebezpečných prvků.'
        if self.focus_mode:
            return 'Focus režim je aktivní: sleduj omezení obsahu a používej pauzy.'
        return 'MindFree browser zobrazuje čistou verzi webu bez trackerů a doporučení.'

    def toggle_focus(self):
        self.focus_mode = not self.focus_mode
        if self.focus_mode:
            self.notify('Focus session started', 'MindFree ti pomáhá lépe využít čas.')
        else:
            self.notify('Focus session stopped', 'Skvělé, že se staráš o svou pozornost.')
        self.update_status_labels()
        self.save_data()

    def reset_timer(self):
        self.total_minutes = 0
        self.session_seconds = 0
        self.update_status_labels()
        self.save_data()

    def normalize_url(self, url):
        if not url:
            return ''
        url = url.strip()
        if not re.match(r'^https?://', url):
            url = 'https://' + url
        return url

    def open_url(self, url_value):
        url = self.normalize_url(url_value)
        if not url:
            self.status_message = 'Zadej platnou URL adresu.'
            return
        self.current_url = url
        self.status_message = f'Načítám {url} ...'
        self.browser_content = 'Načítám stránku, chvilka prosím...'
        content = self.fetch_url(url)
        self.browser_content = content
        self.status_message = f'Načteno {url}'
        self.save_data()

    def fetch_url(self, url):
        try:
            request = Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (MindFree Browser)'
            })
            context = ssl.create_default_context()
            with urlopen(request, timeout=12, context=context) as response:
                raw = response.read().decode('utf-8', errors='ignore')
        except (HTTPError, URLError, OSError) as exc:
            return f'Nelze načíst stránku: {exc}'
        html = self.sanitize_html(raw)
        return self.format_html_to_text(html, url)

    def sanitize_html(self, html):
        if self.block_trackers:
            html = re.sub(r'(?is)<script[^>]+(?:google-analytics|googletagmanager|ga\.js|gtag\.js|analytics\.js|doubleclick\.net|facebook\.net|facebook\.com|googlesyndication|adsbygoogle|ads/google|pixel)[^>]*>.*?</script>', '', html)
            html = re.sub(r'(?is)<[^>]+(?:src|href)=["\']?(?:https?:)?//(?:.*?(?:google-analytics|doubleclick\.net|facebook\.net|facebook\.com|googlesyndication|adsbygoogle|analytics|tracking|pixel))[^>]*>', '', html)
        if self.limit_recommendations:
            html = re.sub(r'(?is)<(aside|section|div)[^>]*(recommended|recommendation|upnext|suggested|watchnext|explore|sidebar|related)[^>]*>.*?</\1>', '', html)
            html = re.sub(r'(?is)<(p|div|span)[^>]*(recommended|suggested|related)[^>]*>.*?</\1>', '', html)
        if self.block_scroll:
            html = re.sub(r'(?is)<script[^>]*>.*?(scroll|wheel|infinite|IntersectionObserver).*?</script>', '', html)
        html = re.sub(r'(?is)<(script|style|noscript|iframe|object|embed|form|button|input|svg|video|audio)[^>]*>.*?</\1>', '', html)
        html = re.sub(r'(?is)<(link|meta|img|input|button)[^>]*>', '', html)
        return html

    def format_html_to_text(self, html, base_url):
        title = re.search(r'(?is)<title>(.*?)</title>', html)
        headings = re.findall(r'(?is)<h[1-3][^>]*>(.*?)</h[1-3]>', html)
        links = re.findall(r'(?is)<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html)
        plain = re.sub(r'(?s)<[^>]+>', ' ', html)
        plain = unescape(plain)
        plain = re.sub(r'\s+', ' ', plain).strip()
        result_lines = []
        if title:
            result_lines.append(f'=== {title.group(1).strip()} ===')
        if headings:
            result_lines.append('Nadpisy:')
            for heading in headings[:8]:
                clean_heading = re.sub(r'<[^>]+>', '', unescape(heading)).strip()
                if clean_heading:
                    result_lines.append('- ' + clean_heading)
        if plain:
            snippet = plain[:3200].strip()
            result_lines.append('\n' + snippet + ('...' if len(plain) > 3200 else ''))
        if links:
            result_lines.append('\nOdkazy:')
            for href, text in links[:12]:
                href = href.strip()
                if href.startswith('#'):
                    continue
                destination = urljoin(base_url, href)
                label = re.sub(r'<[^>]+>', '', unescape(text)).strip() or destination
                result_lines.append(f'- {label}: {destination}')
        result_lines.append('\nMindFree režim: stránka byla odladěna pro méně rozptýlení.')
        if self.child_mode:
            result_lines.append('Dětský režim je aktivní: ještě méně rizikových prvků.')
        return '\n'.join(result_lines)

    def save_data(self):
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                'total_minutes': int(self.total_minutes),
                'daily_target': int(self.daily_target),
                'block_trackers': bool(self.block_trackers),
                'block_scroll': bool(self.block_scroll),
                'limit_recommendations': bool(self.limit_recommendations),
                'mute_notifications': bool(self.mute_notifications),
                'child_mode': bool(self.child_mode),
                'focus_mode': bool(self.focus_mode),
                'block_start': str(self.block_start),
                'block_end': str(self.block_end),
            }
            self.data_file.write_text(__import__('json').dumps(data, indent=2), encoding='utf-8')
        except Exception:
            pass

    def load_data(self):
        if self.data_file.exists():
            try:
                data = __import__('json').loads(self.data_file.read_text(encoding='utf-8'))
                self.total_minutes = data.get('total_minutes', 0)
                self.daily_target = data.get('daily_target', 120)
                self.block_trackers = data.get('block_trackers', True)
                self.block_scroll = data.get('block_scroll', True)
                self.limit_recommendations = data.get('limit_recommendations', True)
                self.mute_notifications = data.get('mute_notifications', False)
                self.child_mode = data.get('child_mode', False)
                self.focus_mode = data.get('focus_mode', False)
                self.block_start = data.get('block_start', '22:00')
                self.block_end = data.get('block_end', '06:00')
            except Exception:
                pass

    def get_hosts_path(self):
        if sys.platform.startswith('win'):
            return Path(r'C:\Windows\System32\drivers\etc\hosts')
        return Path('/etc/hosts')

    def is_admin(self):
        if sys.platform.startswith('win'):
            try:
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            except Exception:
                return False
        return os.geteuid() == 0

    def build_block_entries(self):
        domains = [
            'tiktok.com', 'www.tiktok.com', 'm.tiktok.com',
            'instagram.com', 'www.instagram.com',
            'youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be',
            'facebook.com', 'www.facebook.com',
            'twitter.com', 'www.twitter.com'
        ]
        entries = []
        for domain in domains:
            entries.append(f'127.0.0.1 {domain}')
            entries.append(f'0.0.0.0 {domain}')
        return entries

    def is_block_period(self):
        try:
            now = datetime.now().time()
            start = datetime.strptime(self.block_start, '%H:%M').time()
            end = datetime.strptime(self.block_end, '%H:%M').time()
        except ValueError:
            return False
        if start < end:
            return start <= now < end
        return now >= start or now < end

    def apply_browser_blocks(self):
        hosts_path = self.get_hosts_path()
        if not self.is_admin():
            self.block_status = 'Spusť jako správce pro blokování webů'
            return
        try:
            content = hosts_path.read_text(encoding='utf-8')
        except Exception as exc:
            self.block_status = f'Nelze číst hosts: {exc}'
            return
        if '# MindFree start' in content and '# MindFree end' in content:
            content = re.sub(r'# MindFree start.*?# MindFree end\n?', '', content, flags=re.S)
        lines = [line for line in content.splitlines() if line.strip()]
        lines.append('# MindFree start')
        lines.extend(self.build_block_entries())
        lines.append('# MindFree end')
        try:
            hosts_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            self.block_status = 'Blokování webů aktivní'
        except Exception as exc:
            self.block_status = f'Nelze upravit hosts: {exc}'

    def remove_browser_blocks(self):
        hosts_path = self.get_hosts_path()
        if not self.is_admin():
            self.block_status = 'Spusť jako správce pro odblokování webů'
            return
        try:
            content = hosts_path.read_text(encoding='utf-8')
        except Exception as exc:
            self.block_status = f'Nelze číst hosts: {exc}'
            return
        new_content = re.sub(r'# MindFree start.*?# MindFree end\n?', '', content, flags=re.S)
        try:
            hosts_path.write_text(new_content, encoding='utf-8')
            self.block_status = 'Blokování webů deaktivované'
        except Exception as exc:
            self.block_status = f'Nelze upravit hosts: {exc}'

    def enforce_browser_block(self, dt):
        if self.is_block_period():
            self.apply_browser_blocks()
        else:
            self.remove_browser_blocks()

    def notify(self, title, message):
        if self.mute_notifications:
            return
        try:
            from plyer import notification
            notification.notify(title=title, message=message, timeout=3)
        except Exception:
            pass


if __name__ == '__main__':
    MindFreeApp().run()
