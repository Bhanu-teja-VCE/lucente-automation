import asyncio
import random
from playwright.async_api import async_playwright
from .email_extractor import extract_emails

async def scrape(query: str, location: str, max_results: int) -> list[dict]:
    leads = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context()
        page = await context.new_page()
        
        search_url = f"https://www.google.com/maps/search/{query}+{location}"
        try:
            await page.goto(search_url, timeout=60000)
            await page.wait_for_selector('div[role="feed"]', timeout=15000)
            
            feed = page.locator('div[role="feed"]')
            
            while len(leads) < max_results:
                cards = await feed.locator('.hfpxzc').all()
                if not cards:
                    break
                    
                for i in range(len(leads), min(len(cards), max_results)):
                    card = cards[i]
                    try:
                        await card.click()
                        await asyncio.sleep(random.uniform(1.5, 3.5))
                        
                        name = await card.get_attribute("aria-label")
                        
                        await page.wait_for_selector('h1', timeout=5000)
                        
                        website = ""
                        website_loc = page.locator('a[data-item-id="authority"]')
                        if await website_loc.count() > 0:
                            website = await website_loc.first.get_attribute("href")
                            
                        phone = ""
                        phone_loc = page.locator('button[data-tooltip*="phone"]')
                        if await phone_loc.count() > 0:
                            phone = await phone_loc.first.get_attribute("aria-label")
                            if phone:
                                phone = phone.replace("Phone number: ", "").strip()
                                
                        rating = 0.0
                        review_count = 0
                        rating_loc = page.locator('span[aria-label*="stars"]')
                        if await rating_loc.count() > 0:
                            aria = await rating_loc.first.get_attribute("aria-label")
                            if aria:
                                parts = aria.split(" ")
                                try:
                                    rating = float(parts[0])
                                    review_count = int(parts[2].replace(",", ""))
                                except:
                                    pass
                                    
                        emails = []
                        if website:
                            emails = await extract_emails(website)
                            
                        leads.append({
                            "name": name,
                            "website": website,
                            "phone": phone,
                            "rating": rating,
                            "review_count": review_count,
                            "email": emails[0] if emails else "",
                            "location": location,
                            "niche": query
                        })
                        
                    except Exception as e:
                        print(f"Error extracting card: {e}")
                        continue
                        
                await feed.evaluate("node => node.scrollTop = node.scrollHeight")
                await asyncio.sleep(random.uniform(2.0, 4.0))
                
                new_cards = await feed.locator('.hfpxzc').count()
                if new_cards == len(cards):
                    break
                    
        except Exception as e:
            print(f"Google Maps scrape error: {e}")
            
        finally:
            await browser.close()
            
    return leads[:max_results]
