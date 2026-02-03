# Changelog - 6-Site Expansion

## Version 2.0 - 2026-02-03

### Major Changes: Expanded to 6 Scraping Sites

#### New Sites Added (4)
1. **Carzone.ie** - Commercial vehicles, Mercedes Sprinter focus
   - URL: `https://www.carzone.ie/commercials/used/mercedes-benz/sprinter`
   - Multiple URL attempts for comprehensive coverage
   
2. **CarsIreland.ie** - Minibus body-type filter
   - URL: `https://www.carsireland.ie/used-cars/minibus`
   - Dedicated minibus category
   
3. **Adverts.ie** - Keyword-based search
   - URL: `https://www.adverts.ie/results/minibus`
   - Popular with private sellers
   
4. **Autoline24.ie** - Commercial vehicles
   - Multiple commercial vehicle URLs
   - Specializes in commercial grade vehicles

#### Updated Sites (1)
- **DoneDeal** - Changed from cars to coaches category
  - Old URL: `https://www.donedeal.ie/cars?bodyType=Minibus`
  - New URL: `https://www.donedeal.ie/coaches`
  - Reason: Prioritizes coaches & buses, skips passenger cars

#### Unchanged Sites (1)
- **UsedCarsNI** - Continues as before
  - URL: `https://www.usedcarsni.com/search?bodytype=minibus`

### Feature Enhancements

#### Scraping Improvements
- All new scrapers use same robust framework:
  - Retry logic with exponential backoff
  - Rate limiting per domain
  - Browser fingerprinting
  - Multiple selector fallbacks
  - Graceful error handling

#### Scheduling Changes
- **Previous:** Daily runs recommended
- **New:** Every 6 hours recommended (00:00, 06:00, 12:00, 18:00 UTC)
- **Benefit:** 4 scrapes/day × 6 sites = 24 data collection points daily

#### Code Structure
New scraper methods added:
- `scrape_carzone()` - Carzone commercials scraper
- `scrape_carsireland()` - CarsIreland minibus scraper
- `scrape_adverts()` - Adverts.ie keyword scraper
- `scrape_autoline24()` - Autoline24 commercial scraper

Updated methods:
- `run()` - Now calls all 6 scrapers sequentially
- Module docstring - Updated to reflect 6 sites
- Class docstring - Updated site list

### Documentation Updates

All documentation files updated to reflect 6-site expansion:

#### README.md
- Updated "Scraped Websites" section with all 6 sites
- Added 6-hour scheduling recommendation
- Updated features list

#### USAGE.md
- Expanded "What Sites Are Scraped?" section
- Added detailed scheduling instructions (every 6 hours)
- Updated setup instructions

#### SITES.md
- Added comprehensive details for all 4 new sites
- Explained category strategy for each site
- Added scraping schedule section

#### ANSWER.md
- Updated quick reference table with 6 sites
- Added category strategy explanation
- Added scraping schedule details

### Technical Details

#### Database
- Schema unchanged (backward compatible)
- All 12 fields remain the same
- `source` field now tracks 6 different sites

#### Performance
- Polite delays between sites (2-5 seconds)
- Rate limiting per domain (min 2 seconds)
- Total scrape time: ~2-3 minutes for all 6 sites

#### Testing
- All existing tests pass
- Tests remain independent of actual scraping
- Database operations verified

### Migration Notes

#### For Existing Users
- No breaking changes
- Existing database continues to work
- New listings will have new source values
- Simply update code and restart scraper

#### Deployment
1. Pull latest changes
2. Restart scraper (no config changes needed)
3. Consider updating schedule to every 6 hours

### Market Coverage

With 6 sites, the bot now provides:
- ✅ Complete Republic of Ireland coverage (5 sites)
- ✅ Northern Ireland coverage (1 site)
- ✅ Coaches & buses priority (DoneDeal)
- ✅ Commercial vehicle focus (Carzone, Autoline24)
- ✅ Private seller coverage (Adverts.ie)
- ✅ Dealer coverage (Carzone, CarsIreland, Autoline24)
- ✅ Cross-border price comparison (€ and £)

### Summary Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Sites scraped | 2 | 6 | +200% |
| Data sources | 2 | 6 | +200% |
| Category focus | Cars | Coaches/Buses | Improved |
| Recommended runs/day | 1 | 4 | +300% |
| Data points/day | 2 | 24 | +1100% |

### Next Steps

Recommended actions:
1. Update PythonAnywhere schedule to every 6 hours
2. Monitor new sites for listing quality
3. Adjust scraping intervals if needed
4. Consider adding pagination support in future

---

**Version:** 2.0  
**Date:** 2026-02-03  
**Status:** ✅ Production Ready  
**Breaking Changes:** None
