import asyncio
import random
import re
import os
from playwright.async_api import async_playwright

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

async def scrape(query: str, location: str, max_results: int) -> list[dict]:
    leads = []
    session_file = "instagram_session.json"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context()
        
        if os.path.exists(session_file):
            await context.add_cookies(eval(open(session_file).read()))
            
        page = await context.new_page()
        
        try:
            await page.goto(f"https://www.instagram.com/explore/tags/{query}/", timeout=60000)
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            if "login" in page.url:
                print("Instagram login required. Please run login script manually to generate session.")
                return []
                
            post_links = set()
            while len(post_links) < max_results:
                links = await page.locator('a[href^="/p/"]').all()
                for link in links:
                    href = await link.get_attribute("href")
                    if href:
                        post_links.add(href)
                if len(post_links) >= max_results:
                    break
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(random.uniform(1.5, 3.5))
                
            post_links = list(post_links)[:max_results]
            
            for link in post_links:
                try:
                    await page.goto(f"https://www.instagram.com{link}")
                    await asyncio.sleep(random.uniform(1.5, 3.0))
                    
                    user_link = page.locator('header a').first
                    username = await user_link.text_content()
                    
                    await user_link.click()
                    await asyncio.sleep(random.uniform(2.0, 4.0))
                    
                    bio_loc = page.locator('h1 + div')
                    bio = ""
                    if await bio_loc.count() > 0:
                        bio = await bio_loc.first.text_content()
                        
                    emails = re.findall(EMAIL_REGEX, bio)
                    
                    leads.append({
                        "name": username,
                        "raw_bio": bio,
                        "email": emails[0] if emails else "",
                        "niche": query,
                        "location": location
                    })
                    
                except Exception as e:
                    print(f"Error extracting IG profile: {e}")
                    continue
                    
        except Exception as e:
            print(f"Instagram scrape error: {e}")
            
        finally:
            await browser.close()
            
    return leads
