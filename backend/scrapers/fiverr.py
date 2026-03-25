import asyncio
import random
from playwright.async_api import async_playwright

async def scrape(query: str, location: str, max_results: int) -> list[dict]:
    leads = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            await page.goto(f"https://www.fiverr.com/search/gigs?query={query}&seller_location=IN", timeout=60000)
            await asyncio.sleep(random.uniform(3.0, 5.0))
            
            while len(leads) < max_results:
                cards = await page.locator('.gig-card-layout').all()
                if not cards:
                    break
                    
                for card in cards:
                    if len(leads) >= max_results:
                        break
                    try:
                        seller_loc = card.locator('.seller-name')
                        seller = await seller_loc.text_content() if await seller_loc.count() > 0 else ""
                        
                        title_loc = card.locator('h3')
                        title = await title_loc.text_content() if await title_loc.count() > 0 else ""
                        
                        price_loc = card.locator('.price')
                        price = await price_loc.text_content() if await price_loc.count() > 0 else ""
                        
                        rating_loc = card.locator('.rating-wrapper strong')
                        rating = float(await rating_loc.text_content()) if await rating_loc.count() > 0 else 0.0
                        
                        review_loc = card.locator('.rating-wrapper span')
                        review_text = await review_loc.text_content() if await review_loc.count() > 0 else "0"
                        review_count = int(review_text.replace("(", "").replace(")", "").replace(",", "")) if review_text else 0
                        
                        leads.append({
                            "name": seller.strip(),
                            "raw_bio": title.strip(),
                            "hourly_rate": price.strip(),
                            "rating": rating,
                            "review_count": review_count,
                            "niche": query,
                            "location": "India"
                        })
                    except Exception as e:
                        print(f"Error extracting Fiverr card: {e}")
                        
                next_btn = page.locator('.pagination-arrow-right')
                if await next_btn.count() > 0 and not await next_btn.is_disabled():
                    await next_btn.click()
                    await asyncio.sleep(random.uniform(3.0, 5.0))
                else:
                    break
                    
        except Exception as e:
            print(f"Fiverr scrape error: {e}")
            
        finally:
            await browser.close()
            
    return leads
