# Usage Guide for MiniBus-Bot-Scraper

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py
```

### PythonAnywhere Setup

1. **Upload Files**
   - Upload `scraper.py` and `requirements.txt` to your PythonAnywhere account

2. **Install Dependencies**
   ```bash
   pip3 install --user -r requirements.txt
   ```

3. **Schedule Daily Run**
   - Go to the "Tasks" tab in PythonAnywhere
   - Add a new scheduled task:
     ```
     python3 /home/yourusername/scraper.py
     ```
   - Set the time (e.g., 03:00 UTC for daily runs)

## Output Files

### Database: `minibus_listings.db`
SQLite database with all historical listing data:
- Tracks every ad's lifecycle
- Records first and last seen dates
- Marks ads as active/inactive
- Stores comprehensive vehicle data: year, mileage, seats, fuel type, transmission, color, location, seller type, description

### Excel Export: `minibus_listings.xlsx`
Daily snapshot with:
- All listings (active and inactive)
- All vehicle data fields for filtering and analysis
- Duration calculation showing how long each ad has been tracked
- Easy to analyze in Excel or Google Sheets

## Database Logic

### New Listings
When a new minibus ad is discovered:
- `first_seen_date` = today
- `last_seen_date` = today
- `is_active` = 1 (True)

### Existing Listings
When an ad that's already in the database is found again:
- `last_seen_date` = today (updated)
- `is_active` = 1 (remains active)
- Title and price are updated

### Missing Listings
When an ad in the database is NOT found in today's scrape:
- `is_active` = 0 (False)
- Other fields remain unchanged
- Preserved in database for historical tracking

## Duration Calculation

The `duration_days` column in the Excel export shows:
- **Active listings**: Days from `first_seen_date` to today
- **Inactive listings**: Days from `first_seen_date` to `last_seen_date`

This gives you insights into:
- How long ads typically stay active
- Price trends over time
- Market velocity

## Politeness Features

The scraper implements responsible web scraping:
- **Random delays**: 2-5 seconds between requests
- **User-Agent rotation**: Uses 12 different modern browser signatures
- **Timeout handling**: 30-second timeout per request
- **Error handling**: Gracefully handles network failures
- **Retry logic**: Exponential backoff for failed requests (max 3 attempts)
- **Rate limiting**: Minimum 2 seconds between requests to same domain
- **Session persistence**: Maintains cookies for natural browsing
- **Anti-blocking detection**: Handles 403/429 responses automatically

## Collected Data Fields

The scraper extracts the following information for each minibus listing:
- **Basic Info**: URL, Title, Price
- **Vehicle Specs**: Year, Mileage, Number of Seats
- **Technical**: Fuel Type, Transmission
- **Appearance**: Color
- **Listing Details**: Location, Seller Type, Description
- **Tracking**: First Seen Date, Last Seen Date, Active Status

## Customization

### Adjust Sleep Intervals
Edit the `polite_sleep()` call in `scraper.py`:
```python
self.polite_sleep(min_seconds=3.0, max_seconds=7.0)  # Increase for slower scraping
```

### Modify Retry Attempts
Change `max_retries` in `make_request_with_retry()`:
```python
response = self.make_request_with_retry(url, max_retries=5)  # Default is 3
```

### Change Database Location
Initialize with a custom path:
```python
scraper = MiniBusScraper(db_path="/path/to/custom.db")
```

### Modify Excel Output Name
```python
scraper.export_to_excel(output_file="custom_name.xlsx")
```

## Troubleshooting

### Getting blocked (403/429 errors)
- The scraper automatically retries with backoff
- If persistent, increase sleep intervals to 5-10 seconds
- Reduce scraping frequency (daily instead of hourly)
- Check if your IP is temporarily rate-limited

### No listings found
- Check internet connectivity
- Verify website URLs are still valid in a browser
- Websites may have changed their HTML structure
- Check the console output for error messages

### Database locked error
- Close any programs viewing the database
- On PythonAnywhere, ensure no other instances are running

### Excel export fails
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Check write permissions in the directory

## Testing

Run the test suite to verify functionality:
```bash
python test_scraper.py
```

This tests:
- Database initialization with new schema
- CRUD operations with all data fields
- Excel export with comprehensive columns
- Inactive listing detection
- Anti-blocking components

## Data Analysis Ideas

With the accumulated comprehensive data, you can:
1. **Price Analysis**: Track price trends for similar vehicles by year, mileage, and seats
2. **Market Timing**: Identify best times to buy when inventory is high
3. **Value Detection**: Spot underpriced listings based on year/mileage/features
4. **Duration Analysis**: Monitor how long listings typically stay active
5. **Geographic Pricing**: Analyze pricing differences between locations (Ireland vs. NI)
6. **Seller Patterns**: Compare dealer vs. private seller pricing and turnover
7. **Specification Trends**: Track popular features (fuel type, transmission, seat capacity)
8. **Mileage Impact**: Correlate mileage with price depreciation
9. **Seasonal Patterns**: Identify seasonal variations in pricing and availability
10. **Color Popularity**: Analyze which colors are most common and their pricing

## Support

For issues or questions, please check:
- The README.md for general information
- This USAGE.md for detailed instructions
- Test your setup with `test_scraper.py`
