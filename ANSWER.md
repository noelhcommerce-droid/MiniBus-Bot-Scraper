# What Sites Is the Bot Scraping?

## Quick Answer

The bot scrapes **2 Irish websites** for minibus listings:

| # | Website | URL | Country | Currency |
|---|---------|-----|---------|----------|
| 1 | **DoneDeal** | https://www.donedeal.ie/cars?bodyType=Minibus | 🇮🇪 Republic of Ireland | € Euro |
| 2 | **UsedCarsNI** | https://www.usedcarsni.com/search?bodytype=minibus | 🇬🇧 Northern Ireland | £ Pound |

## Why These Two Sites?

✅ **Complete Irish Market Coverage** - Covers both Republic of Ireland and Northern Ireland  
✅ **Cross-Border Comparison** - Compare prices in Euro and Pound Sterling  
✅ **Diverse Listings** - Both private sellers and dealers  
✅ **Maximum Selection** - Widest range of minibus options available

## Data Collected from Each Site

For each listing, the bot extracts:
- Price, Year, Mileage
- Number of Seats
- Fuel Type, Transmission
- Color, Location
- Seller Type, Description

## Where to Learn More

📄 **Quick Reference:** See `SITES.md` for detailed information about each website  
📖 **User Guide:** See `USAGE.md` for "What Sites Are Scraped?" section  
📋 **Overview:** See `README.md` for "Scraped Websites" section  
💻 **Code:** See `scraper.py` module and class docstrings

## Technical Details

The scraper uses two dedicated methods:
- `scrape_donedeal()` - Scrapes DoneDeal listings
- `scrape_usedcarsni()` - Scrapes UsedCarsNI listings

Both methods:
- Use retry logic with exponential backoff
- Implement rate limiting (2s minimum between requests)
- Rotate through 12 different User-Agent headers
- Handle browser fingerprinting
- Parse HTML with multiple fallback selectors

---

**Last Updated:** 2026-02-03  
**Status:** ✅ Both sites actively scraped
