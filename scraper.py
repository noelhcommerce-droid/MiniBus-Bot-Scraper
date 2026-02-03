import sqlite3
import cloudscraper
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
        print(f"💾 Saved: {title} (€{price})")
    
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

# --- CarsIreland Scraper Logic ---
def scrape_carsireland():
    print("\n🔎 Connecting to CarsIreland...")
    
    # Target: All Minibuses
    url = "https://www.carsireland.ie/used-cars/minibus"
    
    scraper = cloudscraper.create_scraper() 
    
    try:
        response = scraper.get(url)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Connection Failed.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # CarsIreland Logic: Find ads by their specific container class
        # We look for cards that contain listing details
        ads = soup.find_all("div", class_="vehicle-card")
        
        if not ads:
             # Fallback if class names changed: Look for generic links with prices
             ads = soup.find_all("a", href=True)

        count = 0
        for ad in ads:
            try:
                # Extract Text
                text = ad.get_text().strip()
                
                # Extract Link
                if ad.name == 'a':
                    link = ad['href']
                else:
                    link_tag = ad.find("a", href=True)
                    link = link_tag['href'] if link_tag else None

                if link and "carsireland.ie" not in link:
                    link = "https://www.carsireland.ie" + link

                # Filter for Minibuses
                if link and ("minibus" in text.lower() or "sprinter" in text.lower()):
                    # Extract Price
                    price = 0
                    price_text = [s for s in text.split() if '€' in s]
                    if price_text:
                        # Clean up price string (remove € and commas)
                        clean_price = ''.join(filter(str.isdigit, price_text[0]))
                        if clean_price:
                            price = int(clean_price)
                    
                    # Save
                    save_ad(link, text[:50], price, "Check Ad", "CarsIreland")
                    count += 1
            except:
                continue

        print(f"✅ Scan Complete. Found {count} items on Page 1.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Bot Started (Target: CarsIreland)...")
    init_db()
    scrape_carsireland()
    export_to_excel()
