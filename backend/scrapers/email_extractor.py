import httpx
import re
import asyncio
from bs4 import BeautifulSoup

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
FALSE_POSITIVES = [".png", ".jpg", ".jpeg", ".gif", ".css", ".js", "example.com", "sentry.io"]

async def fetch_html(client, url):
    try:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception:
        return ""

async def extract_emails(url: str) -> list[str]:
    if not url.startswith("http"):
        url = "http://" + url
        
    emails = set()
    async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
        html = await fetch_html(client, url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        found = re.findall(EMAIL_REGEX, text)
        emails.update(found)
        
        # Check contact pages
        links = soup.find_all("a", href=True)
        contact_links = []
        for link in links:
            href = link.get("href", "")
            if any(x in href.lower() for x in ["contact", "about"]):
                if href.startswith("http"):
                    contact_links.append(href)
                else:
                    contact_links.append(url.rstrip("/") + "/" + href.lstrip("/"))
                    
        contact_links = list(set(contact_links))[:3] # Max 3 pages
        
        tasks = [fetch_html(client, link) for link in contact_links]
        results = await asyncio.gather(*tasks)
        
        for res_html in results:
            if res_html:
                res_text = BeautifulSoup(res_html, "html.parser").get_text()
                emails.update(re.findall(EMAIL_REGEX, res_text))
                
    valid_emails = []
    for email in emails:
        email = email.lower()
        if not any(fp in email for fp in FALSE_POSITIVES):
            valid_emails.append(email)
            
    return list(set(valid_emails))[:3]
