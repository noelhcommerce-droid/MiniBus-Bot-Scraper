#!/usr/bin/env python3
"""
Test script for the MiniBusScraper functionality.
Tests database operations without requiring actual web scraping.
"""

import os
import sys
from datetime import date
from scraper import MiniBusScraper


def test_database_operations():
    """Test the database initialization and CRUD operations."""
    print("Testing database operations...")
    
    # Use a test database
    test_db = "test_minibus.db"
    
    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Initialize scraper with test database
    scraper = MiniBusScraper(db_path=test_db)
    
    # Test 1: Add new listings
    print("\n1. Testing adding new listings...")
    test_listings_day1 = [
        {
            'url': 'https://example.com/listing1',
            'title': 'Mercedes Sprinter Minibus 2018',
            'price': '€25,000',
            'source': 'TestSite'
        },
        {
            'url': 'https://example.com/listing2',
            'title': 'Ford Transit Minibus 2019',
            'price': '€28,000',
            'source': 'TestSite'
        }
    ]
    
    scraper.update_database(test_listings_day1)
    
    # Test 2: Update existing listing and add new one
    print("\n2. Testing updating existing listing...")
    test_listings_day2 = [
        {
            'url': 'https://example.com/listing1',
            'title': 'Mercedes Sprinter Minibus 2018 - UPDATED',
            'price': '€24,500',
            'source': 'TestSite'
        },
        {
            'url': 'https://example.com/listing3',
            'title': 'Volkswagen Crafter Minibus 2020',
            'price': '€32,000',
            'source': 'TestSite'
        }
    ]
    
    scraper.update_database(test_listings_day2)
    
    # Verify that listing2 was marked as inactive
    print("\n2.5. Verifying inactive listing...")
    import sqlite3
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT is_active FROM listings WHERE url = ?", ('https://example.com/listing2',))
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "listing2 should exist in database"
    assert result[0] == 0, "listing2 should be marked as inactive (is_active=0)"
    print("✓ listing2 correctly marked as inactive")
    
    # Test 3: Export to Excel
    print("\n3. Testing Excel export...")
    test_excel = "test_output.xlsx"
    scraper.export_to_excel(output_file=test_excel)
    
    # Verify files were created
    assert os.path.exists(test_db), "Database file was not created"
    assert os.path.exists(test_excel), "Excel file was not created"
    
    # Test 4: Verify database contents
    print("\n4. Verifying database contents...")
    import pandas as pd
    conn = sqlite3.connect(test_db)
    df = pd.read_sql_query("SELECT * FROM listings", conn)
    conn.close()
    
    assert len(df) == 3, f"Expected 3 listings, found {len(df)}"
    assert df['is_active'].sum() == 2, f"Expected 2 active listings, found {df['is_active'].sum()}"
    assert (df['is_active'] == 0).sum() == 1, f"Expected 1 inactive listing, found {(df['is_active'] == 0).sum()}"
    print(f"✓ Database has {len(df)} listings (2 active, 1 inactive)")
    
    # Test 5: Verify Excel structure
    print("\n5. Verifying Excel file structure...")
    df_excel = pd.read_excel(test_excel, engine='openpyxl')
    expected_columns = ['url', 'title', 'price', 'first_seen_date', 'last_seen_date', 'duration_days', 'is_active']
    assert list(df_excel.columns) == expected_columns, f"Excel columns mismatch. Expected {expected_columns}, got {list(df_excel.columns)}"
    assert 'duration_days' in df_excel.columns, "duration_days column missing from Excel"
    assert len(df_excel) == 3, f"Expected 3 rows in Excel, found {len(df_excel)}"
    print(f"✓ Excel file has correct structure with {len(df_excel)} rows")
    
    print("\n✓ All tests passed!")
    print(f"✓ Database created: {test_db}")
    print(f"✓ Excel file created: {test_excel}")
    
    # Cleanup
    print("\nCleaning up test files...")
    if os.path.exists(test_db):
        os.remove(test_db)
    if os.path.exists(test_excel):
        os.remove(test_excel)
    
    print("✓ Test cleanup complete!")
    

def test_scraper_components():
    """Test individual scraper components."""
    print("\nTesting scraper components...")
    
    scraper = MiniBusScraper(db_path="test_components.db")
    
    # Test random headers generation
    headers1 = scraper.get_random_headers()
    headers2 = scraper.get_random_headers()
    
    assert 'User-Agent' in headers1, "User-Agent not in headers"
    assert 'Accept' in headers1, "Accept not in headers"
    print("✓ Random headers generation works")
    
    # Cleanup
    if os.path.exists("test_components.db"):
        os.remove("test_components.db")
    
    print("✓ Component tests passed!")


if __name__ == "__main__":
    try:
        test_database_operations()
        test_scraper_components()
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
