def scrape_donedeal():
    print("🔎 Scanning DoneDeal (Debug Mode)...")
    # Broader search URL to ensure we find SOMETHING
    url = "https://www.donedeal.ie/coaches?words=minibus"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 Status Code: {response.status_code}") # 200 means success
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"📄 Page Title Found: {soup.title.string.strip()}") # Proves we are on the site
        
        # Updated 2026 Selectors (DoneDeal often changes these)
        # We look for ANY list item that might be an ad
        cards = soup.find_all("li", class_=lambda x: x and "SearchCard" in x)
        
        count = 0
        if not cards:
            print("⚠️ No ads found with 'SearchCard' tag. Trying fallback...")
            # Fallback: Try finding standard links
            cards = soup.find_all("a", href=True)
            
        for card in cards:
            try:
                # Basic text extraction
                text_content = card.get_text()
                if "Sprinter" in text_content or "Minibus" in text_content:
                    # It's a match!
                    link = card.get('href')
                    if link and not link.startswith('http'):
                        link = "https://www.donedeal.ie" + link
                        
                    save_ad(link, "Found Debug Ad", 0, "Unknown", "DoneDeal")
                    count += 1
            except:
                continue
                
        print(f"✅ DoneDeal Scan Complete. Found {count} potential items.")

    except Exception as e:
        print(f"❌ Error: {e}")
