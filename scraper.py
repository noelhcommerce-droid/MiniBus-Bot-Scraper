import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import os

# Database Setup
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
        # Update existing ad (Seen again today)
        c.execute("UPDATE listings SET last_seen=?, active=1 WHERE url=?", (today, url))
        print(f"🔄 Updated: {title}")
    else:
        # Insert new ad
        c.execute("INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
                  (url, title, price, seats, today, today, source))
        print(f"🆕 Found: {title}")
    
    conn.commit()
    conn.close()

def export_to_excel():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM listings", conn)
    conn.close()
    
    # Calculate Days on Market
    df['first_seen'] = pd.to_datetime(df['first_seen'])
    df['last_seen'] = pd.to_datetime(df['last_seen'])
    df['days_on_market'] = (df['last_seen'] - df['first_seen']).dt.days
    
    filename = f"Minibus_Market_Report_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)
    print(f"📊 Report generated: {filename}")

# --- Main Execution ---
if __name__ == "__main__":
    print("🔎 Starting Minibus Market Scan...")
    init_db()
    
    # Placeholder for actual scraping logic (to test the DB first)
    # In the next step, we will add the real DoneDeal scraper here.
    # For now, let's inject a TEST DATA to prove it works.
    save_ad("http://test-url.com/123", "2018 Mercedes Sprinter Test", 18500, "16", "Manual_Test")
    
    export_to_excel()
    print("✅ Scan Complete.")
