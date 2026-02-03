# MiniBus-Bot-Scraper

A Python-based web scraper for Irish minibus listings that scrapes comprehensive data from DoneDeal and UsedCarsNI, stores it in a SQLite database, and exports to Excel with duration tracking.

## Scraped Websites

This bot currently scrapes minibus listings from two Irish websites:

1. **[DoneDeal](https://www.donedeal.ie)** 
   - URL: `https://www.donedeal.ie/cars?bodyType=Minibus`
   - Coverage: Republic of Ireland
   - Currency: Euro (€)

2. **[UsedCarsNI](https://www.usedcarsni.com)**
   - URL: `https://www.usedcarsni.com/search?bodytype=minibus`
   - Coverage: Northern Ireland
   - Currency: Pound Sterling (£)

## Features

- **Multi-source scraping**: Scrapes minibus listings from DoneDeal and UsedCarsNI
- **Comprehensive data collection**: Extracts price, year, mileage, number of seats, fuel type, transmission, color, location, seller type, and description
- **Persistent storage**: Uses SQLite database to track all listings over time
- **Intelligent tracking**: 
  - Adds new listings with first_seen date
  - Updates existing listings with last_seen date
  - Marks missing listings as inactive
- **Excel export**: Generates .xlsx file with Duration column showing how long each listing has been active
- **Advanced anti-blocking strategies**: 
  - Request retry with exponential backoff
  - Session persistence with cookie handling
  - 12 rotating modern User-Agent headers
  - Browser fingerprinting headers (Sec-Fetch-*)
  - Per-domain rate limiting (minimum 2 seconds between requests)
  - Automatic detection and handling of 403/429 responses
- **PythonAnywhere ready**: Optimized to run as a single script on PythonAnywhere

## Installation

1. Clone the repository:
```bash
git clone https://github.com/noelhcommerce-droid/MiniBus-Bot-Scraper.git
cd MiniBus-Bot-Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the scraper locally

```bash
python scraper.py
```

### Setting up on PythonAnywhere

1. Upload `scraper.py` and `requirements.txt` to your PythonAnywhere account
2. Install dependencies in a Bash console:
   ```bash
   pip3 install --user -r requirements.txt
   ```
3. Schedule a daily task:
   - Go to the "Tasks" tab
   - Add a new scheduled task with command: `python3 /home/yourusername/scraper.py`
   - Set the time for daily execution

## Database Schema

The SQLite database (`minibus_listings.db`) contains a single table with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| url | TEXT | Primary key - Unique URL of the listing |
| title | TEXT | Title/description of the minibus |
| price | TEXT | Price information (€ or £) |
| year | TEXT | Year/registration year of the vehicle |
| mileage | TEXT | Mileage/odometer reading |
| num_seats | TEXT | Number of seats/passenger capacity |
| fuel_type | TEXT | Fuel type (Diesel, Petrol, etc.) |
| transmission | TEXT | Transmission type (Manual, Automatic) |
| color | TEXT | Vehicle color |
| location | TEXT | Location/county of the listing |
| seller_type | TEXT | Type of seller (Dealer, Private, Trade) |
| description | TEXT | Additional description/notes |
| first_seen_date | TEXT | ISO date when listing was first discovered |
| last_seen_date | TEXT | ISO date when listing was last seen |
| is_active | INTEGER | 1 if active, 0 if no longer available |

## Output

The script generates two outputs:

1. **SQLite Database** (`minibus_listings.db`): Persistent storage of all listings with comprehensive vehicle data
2. **Excel File** (`minibus_listings.xlsx`): Exportable spreadsheet with:
   - All listing information including year, mileage, seats, fuel type, transmission, color, location, seller type, and description
   - `duration_days` column showing how long each listing has been active
   - Formatted for easy analysis and filtering

## Logic Flow

1. **Scraping**: Fetches listings from DoneDeal and UsedCarsNI with polite delays
2. **Database Update**:
   - New listings → Added with `first_seen_date = today`
   - Existing listings → Updated with `last_seen_date = today`
   - Missing listings → Marked with `is_active = 0`
3. **Excel Export**: Generates comprehensive report with duration calculations

## Anti-Blocking Strategies

The scraper implements multiple strategies to avoid being blocked:

### Request Management
- **Exponential backoff**: Retries failed requests with increasing delays (2^n + random jitter)
- **Rate limiting**: Enforces minimum 2-second delay between requests to the same domain
- **Session persistence**: Maintains cookies across requests for natural browsing behavior
- **Random delays**: 2-5 second pauses between scraping operations

### Browser Simulation
- **12 User-Agent rotation**: Cycles through modern Chrome, Firefox, Safari, Edge, Opera, and Vivaldi browsers
- **Complete headers**: Includes Accept, Accept-Language, Accept-Encoding, Cache-Control
- **Browser fingerprinting**: Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-User headers
- **DNT header**: Do Not Track flag for privacy compliance

### Error Handling
- **403 Forbidden**: Automatic retry with backoff
- **429 Rate Limited**: Extended backoff (2^(n+1) seconds)
- **Content validation**: Verifies HTML responses to detect soft blocks
- **Graceful degradation**: Continues scraping other sources if one fails

### Best Practices
- Maximum 3 retry attempts per request
- 30-second timeout per request
- Validates response content-type
- Logs all blocking attempts for monitoring

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- pandas
- openpyxl
- lxml

## Troubleshooting

### Getting Blocked?
If you receive 403 or 429 errors consistently:
1. Increase the `min_seconds` and `max_seconds` in `polite_sleep()` calls (e.g., 5-10 seconds)
2. Reduce scraping frequency (run daily instead of hourly)
3. Check if your IP is rate-limited (try from a different network)
4. Ensure you're not running multiple instances simultaneously

### No Data Extracted?
- Website HTML structure may have changed
- Check if websites are accessible in your browser
- Look for HTML class name changes in browser inspector
- Update the CSS selectors in scraper methods if needed

### Database Errors?
- Ensure write permissions in the directory
- Close any programs viewing the database file
- Delete and regenerate the database if schema changed

## License

This project is provided as-is for personal use.

## Disclaimer

Please ensure your web scraping activities comply with the terms of service of the websites being scraped. This script implements polite scraping practices (random delays, User-Agent rotation, rate limiting), but users are responsible for ethical and legal use.