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

### Excel Export: `minibus_listings.xlsx`
Daily snapshot with:
- All listings (active and inactive)
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
- **User-Agent rotation**: Uses 5 different browser signatures
- **Timeout handling**: 30-second timeout per request
- **Error handling**: Gracefully handles network failures

## Customization

### Adjust Sleep Intervals
Edit the `polite_sleep()` call in `scraper.py`:
```python
self.polite_sleep(min_seconds=3.0, max_seconds=7.0)  # Increase for slower scraping
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

### No listings found
- Check internet connectivity
- Verify website URLs are still valid
- Websites may have changed their HTML structure

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
- Database initialization
- CRUD operations
- Excel export
- Inactive listing detection

## Data Analysis Ideas

With the accumulated data, you can:
1. Track price trends for similar vehicles
2. Identify best times to buy (when inventory is high)
3. Spot underpriced listings
4. Monitor how long listings typically stay active
5. Analyze geographic pricing differences (Ireland vs. NI)

## Support

For issues or questions, please check:
- The README.md for general information
- This USAGE.md for detailed instructions
- Test your setup with `test_scraper.py`
