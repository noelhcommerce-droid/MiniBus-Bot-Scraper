import sqlite3
import cloudscraper # <--- The new secret weapon
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

# --- Database Setup ---
DB_NAME = "minibus_market.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS listings
                 (url TEXT PRIMARY KEY, title TEXT, price INTEGER, 
                  seats TEXT, first_seen DATE, last_seen DATE, 
                  active BOOLEAN, source TEXT)''')
    conn.commit()
    conn.close()

def save_ad(url, title, price, seats, source):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    today = datetime.now().date()
    
    c.execute("SELECT first_seen FROM listings WHERE url=?", (url,))
    row = c.fetchone()
    
    if row:
        c.execute("UPDATE listings SET last_seen=?, active=1 WHERE url=?", (today, url))
    else:
        c.execute("INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
                  (url, title, price, seats, today, today, source))
        print(f"💾 Saved: {title}")
    
    conn.commit()
    conn.close()

def export_to_excel():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM listings", conn)
    conn.close()
    
    if not df.empty:
        df['first_seen'] = pd.to_datetime(df['first_seen'])
        df['last_seen'] = pd.to_datetime(df['last_seen'])
        df['days_on_market'] = (df['last_seen'] - df['first_seen']).dt.days
        filename = "Minibus_Market_Tracker.xlsx"
        df.to_excel(filename, index=False)
        print(f"📊 Report Updated: {filename}")
    else:
        print("⚠️ Database is empty. No report generated.")

# --- The Scraper Logic (CloudScraper Version) ---
def scrape_donedeal():
    print("\n🔎 Connecting to DoneDeal (Attempting Bypass)...")
    
    # 1. Initialize the Scraper
    scraper = cloudscraper.create_scraper() 
    
    # 2. Target URL
    url = "https://www.donedeal.ie/coaches?words=sprinter"
    
    try:
        # We use scraper.get() instead of requests.get()
        response = scraper.get(url)
        print(f"📡 Status Code: {response.status_code}") 
        
        if response.status_code == 403:
            print("❌ BLOCKED. DoneDeal is blocking PythonAnywhere IPs directly.")
            print("💡 STRATEGY SHIFT: We will switch targets to CarsIreland/Carzone.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        found_count = 0
        all_links = soup.find_all("a", href=True)
        
        for link in all_links:
            href = link['href']
            text = link.get_text().strip()
            
            if ('/coaches/' in href or '/commercials/' in href) and len(text) > 10:
                if 'donedeal.ie' not in href:
                    full_url = "https://www.donedeal.ie" + href
                else:
                    full_url = href
                
                if "sprinter" in text.lower():
                    price = 0
                    try:
                        price_text = [s for s in text.split() if '€' in s]
                        if price_text:
                            price = int(''.join(filter(str.isdigit, price_text[0])))
                    except:
                        price = 0

                    save_ad(full_url, text[:60], price, "Check Ad", "DoneDeal")
                    found_count += 1

        print(f"✅ Scan Complete. Found {found_count} items.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Bot Started...")
    init_db()
    scrape_donedeal()
    export_to_excel()
