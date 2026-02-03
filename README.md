# MiniBus-Bot-Scraper

A Python-based web scraper for Irish minibus listings that scrapes data from DoneDeal and UsedCarsNI, stores it in a SQLite database, and exports to Excel with duration tracking.

## Features

- **Multi-source scraping**: Scrapes minibus listings from DoneDeal and UsedCarsNI
- **Persistent storage**: Uses SQLite database to track all listings over time
- **Intelligent tracking**: 
  - Adds new listings with first_seen date
  - Updates existing listings with last_seen date
  - Marks missing listings as inactive
- **Excel export**: Generates .xlsx file with Duration column showing how long each listing has been active
- **Politeness**: Implements random delays and rotating User-Agent headers to avoid being blocked
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
| price | TEXT | Price information |
| first_seen_date | TEXT | ISO date when listing was first discovered |
| last_seen_date | TEXT | ISO date when listing was last seen |
| is_active | INTEGER | 1 if active, 0 if no longer available |

## Output

The script generates two outputs:

1. **SQLite Database** (`minibus_listings.db`): Persistent storage of all listings
2. **Excel File** (`minibus_listings.xlsx`): Exportable spreadsheet with:
   - All listing information
   - `duration_days` column showing how long each listing has been active
   - Formatted for easy analysis

## Logic Flow

1. **Scraping**: Fetches listings from DoneDeal and UsedCarsNI with polite delays
2. **Database Update**:
   - New listings → Added with `first_seen_date = today`
   - Existing listings → Updated with `last_seen_date = today`
   - Missing listings → Marked with `is_active = 0`
3. **Excel Export**: Generates comprehensive report with duration calculations

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- pandas
- openpyxl
- lxml

## License

This project is provided as-is for personal use.

## Disclaimer

Please ensure your web scraping activities comply with the terms of service of the websites being scraped. This script implements polite scraping practices (random delays, User-Agent rotation), but users are responsible for ethical and legal use.