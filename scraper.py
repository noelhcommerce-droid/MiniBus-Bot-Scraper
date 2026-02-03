#!/usr/bin/env python3
"""
Irish Minibus Listings Scraper
Scrapes minibus listings from DoneDeal and UsedCarsNI, stores them in SQLite,
and exports to Excel with duration tracking.
"""

import sqlite3
import time
import random
from datetime import datetime, date
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


class MiniBusScraper:
    """Scraper for Irish minibus listings with database persistence."""
    
    def __init__(self, db_path: str = "minibus_listings.db"):
        """
        Initialize the scraper with database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                url TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                price TEXT,
                first_seen_date TEXT NOT NULL,
                last_seen_date TEXT NOT NULL,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def get_random_headers(self) -> Dict[str, str]:
        """
        Generate random headers with User-Agent for politeness.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def polite_sleep(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
        """
        Sleep for a random interval to be polite to servers.
        
        Args:
            min_seconds: Minimum sleep time
            max_seconds: Maximum sleep time
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
    
    def scrape_donedeal(self) -> List[Dict[str, str]]:
        """
        Scrape minibus listings from DoneDeal.
        
        Returns:
            List of dictionaries containing listing data
        """
        listings = []
        base_url = "https://www.donedeal.ie"
        search_url = f"{base_url}/cars?bodyType=Minibus"
        
        try:
            print(f"\nScraping DoneDeal: {search_url}")
            response = requests.get(search_url, headers=self.get_random_headers(), timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # DoneDeal listings are typically in cards or list items
            # This is a generic approach that may need adjustment based on actual HTML structure
            listing_cards = soup.find_all('li', class_='card')
            
            if not listing_cards:
                # Try alternative selectors
                listing_cards = soup.find_all('div', class_='listing')
            
            print(f"Found {len(listing_cards)} potential listings on DoneDeal")
            
            for card in listing_cards:
                try:
                    # Extract URL
                    link_tag = card.find('a', href=True)
                    if not link_tag:
                        continue
                    
                    url = urljoin(base_url, link_tag['href'])
                    
                    # Extract title
                    title_tag = card.find(['h3', 'h2', 'a'])
                    title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
                    
                    # Extract price
                    price_tag = card.find(class_=['price', 'listing-price'])
                    if not price_tag:
                        price_tag = card.find(string=lambda text: text and '€' in text)
                    price = price_tag.get_text(strip=True) if price_tag else "Price on request"
                    
                    listings.append({
                        'url': url,
                        'title': title,
                        'price': price,
                        'source': 'DoneDeal'
                    })
                except Exception as e:
                    print(f"Error parsing DoneDeal listing: {e}")
                    continue
            
            print(f"Successfully extracted {len(listings)} listings from DoneDeal")
            
        except requests.RequestException as e:
            print(f"Error scraping DoneDeal: {e}")
        
        return listings
    
    def scrape_usedcarsni(self) -> List[Dict[str, str]]:
        """
        Scrape minibus listings from UsedCarsNI.
        
        Returns:
            List of dictionaries containing listing data
        """
        listings = []
        base_url = "https://www.usedcarsni.com"
        search_url = f"{base_url}/search?bodytype=minibus"
        
        try:
            print(f"\nScraping UsedCarsNI: {search_url}")
            response = requests.get(search_url, headers=self.get_random_headers(), timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # UsedCarsNI listings - generic approach
            listing_cards = soup.find_all('div', class_=['vehicle-card', 'car-item', 'listing'])
            
            if not listing_cards:
                # Try alternative selectors
                listing_cards = soup.find_all('article')
            
            print(f"Found {len(listing_cards)} potential listings on UsedCarsNI")
            
            for card in listing_cards:
                try:
                    # Extract URL
                    link_tag = card.find('a', href=True)
                    if not link_tag:
                        continue
                    
                    url = urljoin(base_url, link_tag['href'])
                    
                    # Extract title
                    title_tag = card.find(['h3', 'h2', 'h4'])
                    title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
                    
                    # Extract price
                    price_tag = card.find(class_=['price', 'vehicle-price'])
                    if not price_tag:
                        price_tag = card.find(string=lambda text: text and '£' in text)
                    price = price_tag.get_text(strip=True) if price_tag else "Price on request"
                    
                    listings.append({
                        'url': url,
                        'title': title,
                        'price': price,
                        'source': 'UsedCarsNI'
                    })
                except Exception as e:
                    print(f"Error parsing UsedCarsNI listing: {e}")
                    continue
            
            print(f"Successfully extracted {len(listings)} listings from UsedCarsNI")
            
        except requests.RequestException as e:
            print(f"Error scraping UsedCarsNI: {e}")
        
        return listings
    
    def update_database(self, listings: List[Dict[str, str]]):
        """
        Update database with scraped listings following the logic:
        - New ads: Add with first_seen = today
        - Existing ads: Update last_seen = today
        - Missing ads: Set is_active = False
        
        Args:
            listings: List of listing dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        today = date.today().isoformat()
        
        # Get all currently active URLs from database
        cursor.execute("SELECT url FROM listings WHERE is_active = 1")
        active_urls = {row[0] for row in cursor.fetchall()}
        
        # Track URLs found in current scrape
        found_urls = set()
        
        # Process each scraped listing
        for listing in listings:
            url = listing['url']
            found_urls.add(url)
            
            # Check if listing exists in database
            cursor.execute("SELECT url FROM listings WHERE url = ?", (url,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing listing
                cursor.execute('''
                    UPDATE listings 
                    SET last_seen_date = ?,
                        title = ?,
                        price = ?,
                        is_active = 1
                    WHERE url = ?
                ''', (today, listing['title'], listing['price'], url))
                print(f"Updated: {listing['title'][:50]}...")
            else:
                # Insert new listing
                cursor.execute('''
                    INSERT INTO listings (url, title, price, first_seen_date, last_seen_date, is_active)
                    VALUES (?, ?, ?, ?, ?, 1)
                ''', (url, listing['title'], listing['price'], today, today))
                print(f"Added new: {listing['title'][:50]}...")
        
        # Mark listings not found in current scrape as inactive
        missing_urls = active_urls - found_urls
        for url in missing_urls:
            cursor.execute('''
                UPDATE listings 
                SET is_active = 0
                WHERE url = ?
            ''', (url,))
            print(f"Marked inactive: {url}")
        
        conn.commit()
        
        # Print summary
        cursor.execute("SELECT COUNT(*) FROM listings")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM listings WHERE is_active = 1")
        active = cursor.fetchone()[0]
        
        print(f"\nDatabase summary:")
        print(f"  Total listings: {total}")
        print(f"  Active listings: {active}")
        print(f"  Inactive listings: {total - active}")
        print(f"  New listings found: {len(found_urls - active_urls)}")
        print(f"  Listings marked inactive: {len(missing_urls)}")
        
        conn.close()
    
    def export_to_excel(self, output_file: str = "minibus_listings.xlsx"):
        """
        Export all listings to Excel with Duration column.
        Duration = days between first_seen and last_seen
        
        Args:
            output_file: Path to output Excel file
        """
        conn = sqlite3.connect(self.db_path)
        
        # Read all listings from database
        df = pd.read_sql_query("SELECT * FROM listings", conn)
        conn.close()
        
        if df.empty:
            print("No listings to export.")
            return
        
        # Calculate duration in days
        df['first_seen_date'] = pd.to_datetime(df['first_seen_date'])
        df['last_seen_date'] = pd.to_datetime(df['last_seen_date'])
        
        # For active listings, duration is from first_seen to today
        # For inactive listings, duration is from first_seen to last_seen
        today = pd.Timestamp(date.today())
        df['duration_days'] = df.apply(
            lambda row: (today - row['first_seen_date']).days if row['is_active'] == 1 
            else (row['last_seen_date'] - row['first_seen_date']).days,
            axis=1
        )
        
        # Convert is_active from 0/1 to False/True for better readability
        df['is_active'] = df['is_active'].astype(bool)
        
        # Reorder columns for better readability
        columns = ['url', 'title', 'price', 'first_seen_date', 'last_seen_date', 
                   'duration_days', 'is_active']
        df = df[columns]
        
        # Export to Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"\nExported {len(df)} listings to {output_file}")
        print(f"  Active: {df['is_active'].sum()}")
        print(f"  Inactive: {(~df['is_active']).sum()}")
        
        # Calculate and display average duration if there are valid values
        avg_duration = df['duration_days'].mean()
        if pd.notna(avg_duration):
            print(f"  Average duration: {avg_duration:.1f} days")
        else:
            print(f"  Average duration: N/A")
    
    def run(self):
        """
        Main execution method - scrapes all sources, updates database, exports to Excel.
        """
        print("=" * 60)
        print("Irish Minibus Listings Scraper")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        all_listings = []
        
        # Scrape DoneDeal
        donedeal_listings = self.scrape_donedeal()
        all_listings.extend(donedeal_listings)
        self.polite_sleep()
        
        # Scrape UsedCarsNI
        usedcarsni_listings = self.scrape_usedcarsni()
        all_listings.extend(usedcarsni_listings)
        
        print(f"\n{'=' * 60}")
        print(f"Total listings scraped: {len(all_listings)}")
        print(f"  DoneDeal: {len(donedeal_listings)}")
        print(f"  UsedCarsNI: {len(usedcarsni_listings)}")
        print(f"{'=' * 60}\n")
        
        # Update database
        if all_listings:
            self.update_database(all_listings)
        else:
            print("No listings found. Database not updated.")
        
        # Export to Excel
        self.export_to_excel()
        
        print("\n" + "=" * 60)
        print(f"Scraping completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)


def main():
    """Main entry point for the scraper."""
    scraper = MiniBusScraper()
    scraper.run()


if __name__ == "__main__":
    main()
