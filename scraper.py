import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

# --- CONFIGURATION ---
DB_NAME = "minibus_market.db"
# We overwrite this SINGLE file every day so you don't get clutter
EXCEL_FILENAME = "Minibus_Master_Tracker.xlsx"

# Headers to make the bot look like a real human browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def init_db():
    """Create the database if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # We track: URL (ID), Title, Price, Year, Engine, Mileage, First Seen, Last Seen, Active Status
    c.execute('''CREATE TABLE IF NOT EXISTS listings
                 (url TEXT PRIMARY KEY, title TEXT, price INTEGER, 
                  year TEXT, engine TEXT, mileage TEXT,
                  first_seen DATE, last_seen DATE, 
                  active BOOLEAN, source TEXT)''')
    conn.commit()
    conn.close()

def save_ad(ad_data):
    """Save a single vehicle to the database logic."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    today = datetime.now().date()
    
    # Check if we have seen this specific link before
    c.execute("SELECT first_seen FROM listings WHERE url=?", (ad_data['url'],))
    row = c.fetchone()
    
    if row:
        # We HAVE seen it. Update 'last_seen' to today so we know it's still active.
        c.execute("UPDATE listings SET last_seen=?, active=1, price=? WHERE url=?", 
                  (today, ad_data['price'], ad_data['url']))
        print(f"🔄 Updated: {ad_data['title']}")
    else:
        # New Listing! Insert it.
        c.execute('''INSERT INTO listings VALUES 
                     (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)''',
                  (ad_data['url'], ad_data['title'], ad_data['price'], 
                   ad_data['year'], ad_data['engine'], ad_data['mileage'],
                   today, today, ad_data['source']))
        print(f"🆕 Found: {ad_data['title']} - €{ad_data['price']}")
    
    conn.commit()
    conn.close()

def scrape_donedeal():
    """Scrapes the Coaches/Buses section of DoneDeal."""
    print("🔎 Scanning DoneDeal...")
    # URL for 'Coaches & Buses' searching for 'Sprinter'
    url = "https://www.donedeal.ie/coaches?words=sprinter"
    
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This selector finds the ad cards on DoneDeal (may need tweaking if DD updates layout)
        # We look for links that look like /coaches/view/...
        ads = soup.find_all('a', href=True)
        
        count = 0
        for ad in ads:
            link = ad['href']
            if "/coaches/view/" in link:
                full_url = link if link.startswith("http") else "https://www.donedeal.ie" + link
                
                # Extract Title (Text inside the link)
                title = ad.get_text(strip=True)
                
                # Default values if scraping fails
                price = 0 
                
                # Simple Logic: If it's a Sprinter, save it
                if "sprinter" in title.lower():
                    # Create a data package
                    vehicle = {
                        'url': full_url,
                        'title': title[:50], # Keep title short
                        'price': price,      # Price scraping is complex, placeholder for now
                        'year': "N/A",
                        'engine': "N/A",
                        'mileage': "N/A",
                        'source': "DoneDeal"
                    }
                    save_ad(vehicle)
                    count += 1
                    
        print(f"✅ DoneDeal Scan Complete. Found {count} items.")
        
    except Exception as e:
        print(f"❌ Error scraping DoneDeal: {e}")

def export_master_report():
    """Exports the WHOLE database to a single Excel file."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM listings", conn)
    conn.close()
    
    if df.empty:
        print("⚠️ Database is empty. No report generated.")
        return

    # 1. Calculate 'Days on Market' (Crucial for finding desperate sellers)
    df['first_seen'] = pd.to_datetime(df['first_seen'])
    df['last_seen'] = pd.to_datetime(df['last_seen'])
    df['days_on_market'] = (df['last_seen'] - df['first_seen']).dt.days
    
    # 2. Mark 'Sold' items
    # If an ad wasn't seen today, we assume it's gone (inactive)
    today = pd.to_datetime(datetime.now().date())
    df['status'] = df['last_seen'].apply(lambda x: 'Active' if x == today else 'Sold/Removed')
    
    # 3. overwrite the Master File
    df.to_excel(EXCEL_FILENAME, index=False)
    print(f"📊 Master Report Updated: {EXCEL_FILENAME}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    init_db()
    scrape_donedeal() 
    # Add other sites (Carzone, etc.) here later
    export_master_report()
