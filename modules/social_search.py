
import asyncio
import aiohttp
import json
import os
from typing import List, Dict

from bs4 import BeautifulSoup

async def check_site(session: aiohttp.ClientSession, site: str, data: dict, username: str) -> dict:
    url = data['url'].format(username)
    error_type = data.get('errorType', 'status_code')
    error_msg = data.get('errorMsg')

    try:
        async with session.get(url, timeout=10) as response:
            if error_type == 'status_code':
                if response.status != error_msg:
                     # Scraping
                     text = await response.text()
                     soup = BeautifulSoup(text, 'html.parser')
                     title = soup.title.string.strip() if soup.title else "No Title"
                     try:
                        desc = soup.find("meta", attrs={"name": "description"}).get("content").strip()
                     except:
                        desc = "No Description"
                        
                     return {"site": site, "url": url, "exists": True, "title": title, "desc": desc}
            elif error_type == 'message':
                text = await response.text()
                if error_msg not in text:
                     return {"site": site, "url": url, "exists": True}
    except Exception as e:
        # Ignore errors for now or log them
        pass
    
    return {"site": site, "url": url, "exists": False}

async def search_social(username: str, config: dict = None) -> List[Dict]:
    results = []
    
    # Load site data
    data_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(data_path, 'r') as f:
            sites = json.load(f)
    except FileNotFoundError:
        # Fallback if file missing
        sites = {}

    if not sites:
        return results

    async with aiohttp.ClientSession() as session:
        tasks = []
        for site, data in sites.items():
            tasks.append(check_site(session, site, data, username))
        
        responses = await asyncio.gather(*tasks)
        
        for r in responses:
            if r['exists']:
                results.append(r)
                
    return results

if __name__ == "__main__":
    # Test
    async def main():
        res = await search_social("testuser123")
        print(res)
    asyncio.run(main())
