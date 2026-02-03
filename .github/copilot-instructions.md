"Act as a Data Engineer. I need a Python script to run daily on PythonAnywhere that scrapes Irish minibus listings (e.g., DoneDeal, UsedCarsNI).

Requirements:

Persistence: Use a sqlite3 database to store every ad. Each record needs: url (primary key), title, price, first_seen_date, last_seen_date, and is_active.

Logic: > - If an ad is found and not in the DB, add it with first_seen = today.

If an ad is found and already in the DB, update last_seen = today.

If an ad in the DB is NOT found in today's scrape, set is_active = False.

Excel Export: Every time the script runs, it must generate a .xlsx file using pandas that calculates a 'Duration' column for all listings.

Politeness: Implement random time.sleep() intervals and a random User-Agent header to avoid being blocked.

Environment: Optimize the code to run as a single script on PythonAnywhere."
