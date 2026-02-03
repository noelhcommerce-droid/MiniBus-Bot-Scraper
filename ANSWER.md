# What Sites Is the Bot Scraping?

## Quick Answer

The bot scrapes **6 Irish websites** for minibus and coach listings:

| # | Website | URL | Country | Currency |
|---|---------|-----|---------|----------|
| 1 | **DoneDeal** | https://www.donedeal.ie/coaches | 🇮🇪 Republic of Ireland | € Euro |
| 2 | **UsedCarsNI** | https://www.usedcarsni.com/search?bodytype=minibus | 🇬🇧 Northern Ireland | £ Pound |
| 3 | **Carzone** | https://www.carzone.ie/commercials/used/mercedes-benz/sprinter | 🇮🇪 Republic of Ireland | € Euro |
| 4 | **CarsIreland** | https://www.carsireland.ie/used-cars/minibus | 🇮🇪 Republic of Ireland | € Euro |
| 5 | **Adverts.ie** | https://www.adverts.ie/results/minibus | 🇮🇪 Republic of Ireland | € Euro |
| 6 | **Autoline24** | https://www.autoline24.ie/minibus | 🇮🇪 Republic of Ireland | € Euro |

## Why These Sites?

✅ **Complete Irish Market Coverage** - Covers both Republic of Ireland and Northern Ireland  
✅ **Coaches & Buses Priority** - DoneDeal targets coaches category, not standard cars  
✅ **Commercial Focus** - Carzone and Autoline24 specialize in commercial vehicles  
✅ **Cross-Border Comparison** - Compare prices in Euro and Pound Sterling  
✅ **Diverse Listings** - From private sellers (Adverts.ie) to dealers (Carzone)  
✅ **Maximum Selection** - 6 sources = widest range of minibus/coach options

## Category Strategy

- **DoneDeal:** Coaches & Buses category (skips passenger cars)
- **Carzone:** Commercials, Mercedes Sprinter focus
- **CarsIreland:** Minibus body-type filter
- **Adverts.ie:** Keyword-based (popular with private sellers)
- **UsedCarsNI:** Minibus body type
- **Autoline24:** Commercial vehicles

## Scraping Schedule

**Recommended:** Run every **6 hours** for optimal tracking
- 00:00 UTC (midnight)
- 06:00 UTC (6am)
- 12:00 UTC (noon)
- 18:00 UTC (6pm)

**Result:** 4 scrapes/day × 6 sites = 24 data collection points daily

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

The scraper uses six dedicated methods:
- `scrape_donedeal()` - Scrapes DoneDeal coaches
- `scrape_usedcarsni()` - Scrapes UsedCarsNI listings
- `scrape_carzone()` - Scrapes Carzone commercials
- `scrape_carsireland()` - Scrapes CarsIreland minibuses
- `scrape_adverts()` - Scrapes Adverts.ie keyword results
- `scrape_autoline24()` - Scrapes Autoline24 commercial vehicles

All methods:
- Use retry logic with exponential backoff
- Implement rate limiting (2s minimum between requests)
- Rotate through 12 different User-Agent headers
- Handle browser fingerprinting
- Parse HTML with multiple fallback selectors

---

**Last Updated:** 2026-02-03  
**Status:** ✅ All 6 sites actively scraped  
**Recommended Schedule:** Every 6 hours
