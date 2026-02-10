
import aiohttp
import asyncio
from typing import Dict, List

import dns.resolver

async def check_mx(email: str) -> List[Dict]:
    domain = email.split('@')[-1]
    mx_records = []
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        for rdata in answers:
            mx_records.append({"exchange": str(rdata.exchange), "preference": rdata.preference})
    except Exception as e:
        mx_records.append({"error": f"DNS Error: {str(e)}"})
    return mx_records

async def check_hibp(email: str, api_key: str) -> List[Dict]:
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "Project-Icarus"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            elif response.status == 404:
                return [] # Not pwned
            else:
                # Handle 401, 429, etc.
                return [{"error": f"HIBP Error: {response.status}"}]

async def search_email(email: str, config: Dict) -> Dict:
    results = {
        "email": email,
        "breaches": [],
        "mx_records": [],
        "registered_sites": []
    }
    
    # Check MX
    results["mx_records"] = await check_mx(email)
    
    hibp_key = config.get("api_keys", {}).get("haveibeenpwned")
    if hibp_key and "YOUR_HIBP_API_KEY" not in hibp_key:
        breaches = await check_hibp(email, hibp_key)
        results["breaches"] = breaches
    else:
        results["breaches"] = [{"info": "HIBP API Key not configured or is default."}]

    # Enhanced Social Discovery via Web Search
    from modules import web_search
    social_platforms = {
        "LinkedIn": "linkedin.com",
        "Facebook": "facebook.com",
        "Twitter": "twitter.com",
        "Instagram": "instagram.com",
        "Github": "github.com"
    }
    
    found_profiles = []
    for platform, domain in social_platforms.items():
        res = web_search.search_web(email, config, max_results=1, site_filter=domain)
        if res:
            found_profiles.append({
                "platform": platform,
                "url": res[0]['href'], 
                "title": res[0]['title']
            })
    
    results["social_media_connections"] = found_profiles

    # Placeholder for Holehe-like logic
    # In a real implementation, we would check sites here
    results["registered_sites"].append({"site": "Example Site", "status": "Not Checked (Placeholder)"})

    return results
