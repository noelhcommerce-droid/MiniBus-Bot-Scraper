import sqlite3
import requests
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
    
    # Check if exists
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

# --- The Scraper Logic (Anti-Block Version) ---
def scrape_donedeal():
    print("\n🔎 Connecting to DoneDeal...")
    
    # 1. Broader Search URL (Avoids strict filters that return 0 results)
    url = "https://www.donedeal.ie/coaches?words=sprinter"
    
    # 2. THE FAKE ID (Headers)
    # This makes the bot look like a real Chrome Browser on Windows 10
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    try:
        # Add a small delay to be polite
        time.sleep(2)
        
        response = requests.get(url, headers=headers)
        print(f"📡 Status Code: {response.status_code}") 
        
        if response.status_code == 403:
            print("❌ Still blocked (403). DoneDeal needs a stronger bypass.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Universal Link Finder
        # Finds any link that looks like a commercial vehicle ad
        found_count = 0
        all_links = soup.find_all("a", href=True)
        
        for link in all_links:
            href = link['href']
            text = link.get_text().strip()
            
            # Filter logic: Must be a coach/bus ad and not a dealer homepage
            if ('/coaches/' in href or '/commercials/' in href) and len(text) > 10:
                if 'donedeal.ie' not in href:
                    full_url = "https://www.donedeal.ie" + href
                else:
                    full_url = href
                
                # Check for "Sprinter" in the text to be sure
                if "sprinter" in text.lower():
                     # Price Finder
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

# --- THE START BUTTON ---
if __name__ == "__main__":
    print("🚀 Bot Started...")
    init_db()
    scrape_donedeal()
    export_to_excel()
