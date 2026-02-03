# Scraped Websites

## Overview

The MiniBus-Bot-Scraper scrapes minibus and coach listings from **six Irish websites**:

---

## 1. DoneDeal 🇮🇪

**Website:** [DoneDeal.ie](https://www.donedeal.ie)

**Scraping URL:** 
```
https://www.donedeal.ie/coaches
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** General classified ads platform
- **Category:** Coaches & Buses (prioritized over passenger cars)
- **Listings:** Private sellers and dealers
- **Coverage:** All-Ireland but primarily Republic of Ireland

**Why This Category:**
- Targets coaches and buses specifically
- Skips standard passenger cars and panel vans
- Better ROI for commercial vehicle tracking

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

## 3. Carzone 🇮🇪

**Website:** [Carzone.ie](https://www.carzone.ie)

**Scraping URLs:**
```
https://www.carzone.ie/commercials/used/mercedes-benz/sprinter
https://www.carzone.ie/commercials/minibus
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** Commercial vehicle marketplace
- **Category:** Commercials, Mercedes-Benz Sprinter focus
- **Listings:** Mainly dealers, some private
- **Coverage:** All of Ireland

**Why This Site:**
- Clean, structured URLs
- Easy to target specific years (important for ROI calculations)
- Mercedes Sprinter is a key commercial minibus model
- Template structure: `/commercials/used/mercedes-benz/sprinter/[YEAR]`

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## 4. CarsIreland 🇮🇪

**Website:** [CarsIreland.ie](https://www.carsireland.ie)

**Scraping URL:**
```
https://www.carsireland.ie/used-cars/minibus
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** Used car marketplace
- **Category:** Dedicated minibus body-type filter
- **Listings:** Dealers and private sellers
- **Coverage:** All of Ireland

**Why This Site:**
- Has dedicated "Minibus" body-type filter
- Perfect for market tracking
- Good mix of dealer and private listings

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## 5. Adverts.ie 🇮🇪

**Website:** [Adverts.ie](https://www.adverts.ie)

**Scraping URL:**
```
https://www.adverts.ie/results/minibus
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** General classifieds platform
- **Category:** Keyword-based search (minibus)
- **Listings:** Mainly private sellers
- **Coverage:** All of Ireland

**Why This Site:**
- Keyword-heavy site popular with private sellers
- Often has listings not found on other platforms
- Good for finding private sale opportunities

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## 6. Autoline24.ie 🇮🇪

**Website:** [Autoline24.ie](https://www.autoline24.ie)

**Scraping URLs:**
```
https://www.autoline24.ie/minibus
https://www.autoline24.ie/commercial-vehicles/minibus
```

**Details:**
- **Country:** Republic of Ireland
- **Currency:** Euro (€)
- **Type:** Commercial vehicle marketplace
- **Category:** Commercial vehicles, minibus focus
- **Listings:** Mainly commercial dealers
- **Coverage:** Ireland and international

**Why This Site:**
- Specializes in commercial vehicles
- Good for professional/commercial grade minibuses
- Often has newer models and imports

**Data Extracted:**
- Price, Year, Mileage, Number of Seats
- Fuel Type, Transmission, Color
- Location, Seller Type, Description

---

## Combined Coverage

By scraping all six sites, the bot provides comprehensive coverage of the Irish minibus/coach market:

- ✅ **Republic of Ireland** listings (DoneDeal, Carzone, CarsIreland, Adverts.ie, Autoline24)
- ✅ **Northern Ireland** listings (UsedCarsNI)
- ✅ Both **Euro and Pound** pricing
- ✅ **Private and dealer** listings
- ✅ **Coaches, buses, and commercial minibuses**
- ✅ Cross-border price comparison capability
- ✅ Multiple listing sources = no gaps in market coverage

---

## Scraping Strategy

### Category Focus
- **DoneDeal:** Coaches & Buses category (not standard cars)
- **Carzone:** Commercial vehicles, Sprinter-specific
- **CarsIreland:** Minibus body-type filter
- **Adverts.ie:** Keyword search for broad coverage
- **Autoline24:** Commercial vehicle focus

### Scheduling
- **Recommended:** Run every 6 hours
- **Schedule:** 00:00, 06:00, 12:00, 18:00 UTC
- **Benefit:** 4 scrapes/day × 6 sites = 24 data collection points daily

---

## How It Works

The scraper:
1. Visits each website's coach/minibus search pages
2. Extracts listing cards from the HTML
3. Parses comprehensive vehicle data (12 fields per listing)
4. Stores all listings in a SQLite database
5. Exports to Excel with duration tracking

**Scraping Schedule:** Recommended every 6 hours

**Anti-Blocking:** Implements polite scraping with delays, User-Agent rotation, and retry logic

---

## Adding More Sites

To add additional sites to scrape, you would need to:

1. Create a new method like `scrape_newsite()` in `scraper.py`
2. Define the base URL and search URL
3. Implement the HTML parsing logic for that site's structure
4. Add a call to the new method in the `run()` function

See the existing scraper methods as templates.

---

**Last Updated:** 2026-02-03  
**Sites Active:** 6
