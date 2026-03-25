import asyncio
import random
import os
from playwright.async_api import async_playwright

async def scrape(query: str, location: str, max_results: int) -> list[dict]:
    leads = []
    session_file = "upwork_session.json"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context()
        
        if os.path.exists(session_file):
            await context.add_cookies(eval(open(session_file).read()))
            
        page = await context.new_page()
        
        try:
            await page.goto(f"https://www.upwork.com/search/profiles/?q={query}&loc=india", timeout=60000)
            await asyncio.sleep(random.uniform(3.0, 5.0))
            
            while len(leads) < max_results:
                cards = await page.locator('.up-card-section').all()
                if not cards:
                    break
                    
                for card in cards:
                    if len(leads) >= max_results:
                        break
                    try:
                        name_loc = card.locator('.identity-name')
                        name = await name_loc.text_content() if await name_loc.count() > 0 else ""
                        
                        title_loc = card.locator('.freelancer-title')
                        title = await title_loc.text_content() if await title_loc.count() > 0 else ""
                        
                        rate_loc = card.locator('[data-qa="rate"]')
                        rate = await rate_loc.text_content() if await rate_loc.count() > 0 else ""
                        
                        jss_loc = card.locator('.up-job-success-text')
                        jss = await jss_loc.text_content() if await jss_loc.count() > 0 else ""
                        
                        desc_loc = card.locator('.up-line-clamp-v2')
                        desc = await desc_loc.text_content() if await desc_loc.count() > 0 else ""
                        
                        leads.append({
                            "name": name.strip(),
                            "raw_bio": f"{title.strip()}\\n{desc.strip()}",
                            "hourly_rate": rate.strip(),
                            "response_rate": jss.strip(),
                            "niche": query,
                            "location": "India"
                        })
                    except Exception as e:
                        print(f"Error extracting Upwork card: {e}")
                        
                next_btn = page.locator('.up-pagination-item').filter(has_text="Next")
                if await next_btn.count() > 0 and not await next_btn.is_disabled():
                    await next_btn.click()
                    await asyncio.sleep(random.uniform(3.0, 5.0))
                else:
                    break
                    
        except Exception as e:
            print(f"Upwork scrape error: {e}")
            
        finally:
            await browser.close()
            
    return leads
