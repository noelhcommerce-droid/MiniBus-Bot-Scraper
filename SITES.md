# Scraped Websites

## Overview

The MiniBus-Bot-Scraper currently scrapes minibus listings from **two Irish websites**:

---

## 1. DoneDeal 🇮🇪

**Website:** [DoneDeal.ie](https://www.donedeal.ie)

**Scraping URL:** 
```
https://www.donedeal.ie/cars?bodyType=Minibus
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** General classified ads platform
- **Category:** Cars → Minibus body type
- **Listings:** Private sellers and dealers
- **Coverage:** All-Ireland but primarily Republic of Ireland

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## 2. UsedCarsNI 🇬🇧

**Website:** [UsedCarsNI.com](https://www.usedcarsni.com)

**Scraping URL:**
```
https://www.usedcarsni.com/search?bodytype=minibus
```

**Details:**
- **Country:** Northern Ireland (UK)
- **Currency:** Pound Sterling (£)
- **Type:** Used car marketplace
- **Category:** Body type filter for minibus
- **Listings:** Dealers and private sellers
- **Coverage:** Northern Ireland specifically

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## Combined Coverage

By scraping both sites, the bot provides comprehensive coverage of the Irish minibus market:

- ✅ **Republic of Ireland** listings (DoneDeal)
- ✅ **Northern Ireland** listings (UsedCarsNI)
- ✅ Both **Euro and Pound** pricing
- ✅ **Private and dealer** listings
- ✅ Cross-border price comparison capability

---

## How It Works

The scraper:
1. Visits each website's minibus search page
2. Extracts listing cards from the HTML
3. Parses comprehensive vehicle data (12 fields per listing)
4. Stores all listings in a SQLite database
5. Exports to Excel with duration tracking

**Scraping Schedule:** Designed to run daily (configurable)

**Anti-Blocking:** Implements polite scraping with delays, User-Agent rotation, and retry logic

---

## Adding More Sites

To add additional sites to scrape, you would need to:

1. Create a new method like `scrape_newsite()` in `scraper.py`
2. Define the base URL and search URL
3. Implement the HTML parsing logic for that site's structure
4. Add a call to the new method in the `run()` function

See the existing `scrape_donedeal()` and `scrape_usedcarsni()` methods as templates.

---

**Last Updated:** 2026-02-03
