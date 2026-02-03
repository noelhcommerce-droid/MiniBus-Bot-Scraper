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

# --- The Scraper Logic ---
def scrape_donedeal():
    print("\n🔎 Connecting to DoneDeal...")
    # Using a broad search to ensure we see results
    url = "https://www.donedeal.ie/coaches?words=sprinter"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 Status Code: {response.status_code}") # Should be 200
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2026 Strategy: Find ALL links and filter for 'minibus' terms
        # This bypasses specific class names that might change
        found_count = 0
        all_links = soup.find_all("a", href=True)
        
        for link in all_links:
            href = link['href']
            text = link.get_text().lower()
            
            # Filter: Must be a listing URL and contain relevant text
            if ('/coaches/' in href or '/commercials/' in href) and len(text) > 5:
                # Construct full URL
                if not href.startswith('http'):
                    full_url = "https://www.donedeal.ie" + href
                else:
                    full_url = href
                
                # Simple Price Finder (looks for € symbol in the link text)
                price = 0
                if '€' in text:
                    try:
                        # Extract numbers from text like "€18,500"
                        price_str = ''.join(filter(str.isdigit, text))
                        price = int(price_str)
                    except:
                        price = 0
                
                # Save it!
                save_ad(full_url, text.strip()[:50], price, "Check Ad", "DoneDeal")
                found_count += 1

        print(f"✅ Scan Complete. Found {found_count} potential Sprinters.")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- THE START BUTTON (Main Execution) ---
if __name__ == "__main__":
    print("🚀 Bot Started...")
    init_db()
    scrape_donedeal()  # <--- This was likely missing!
    export_to_excel()
