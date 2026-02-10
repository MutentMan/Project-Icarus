
import phonenumbers
from phonenumbers import geocoder, carrier
import aiohttp
import asyncio
from typing import Dict

async def check_numverify(phone_number: str, api_key: str) -> Dict:
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return {"error": f"NumVerify Error: {response.status}"}
        except Exception as e:
            return {"error": f"Request Failed: {str(e)}"}

async def search_phone(phone_input: str, config: Dict) -> Dict:
    results = {
        "phone": phone_input,
        "valid": False,
        "country": None,
        "location": None,
        "carrier": None,
        "numverify": {}
    }
    
    try:
        parsed_number = phonenumbers.parse(phone_input)
        if phonenumbers.is_valid_number(parsed_number):
            results["valid"] = True
            results["country"] = phonenumbers.region_code_for_number(parsed_number)
            results["location"] = geocoder.description_for_number(parsed_number, "en")
            results["carrier"] = carrier.name_for_number(parsed_number, "en")
            
            # Format to E164 for API usage
            e164_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            
            numverify_key = config.get("api_keys", {}).get("numverify")
            if numverify_key and "YOUR_NUMVERIFY_API_KEY" not in numverify_key:
                results["numverify"] = await check_numverify(e164_number, numverify_key)
            else:
                 results["numverify"] = {"info": "NumVerify API Key not configured or is default."}
            
            # Web Search for Phone
            from modules import web_search
            results["web_mentions"] = web_search.search_web(f'"{e164_number}"', config)
                 
        else:
            results["error"] = "Invalid Phone Number"
            
    except phonenumbers.NumberParseException:
        results["error"] = "Could not parse phone number"
        
    return results
