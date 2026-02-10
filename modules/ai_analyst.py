
import requests
import json
import asyncio
from rich.console import Console
from rich.panel import Panel

console = Console()

async def analyze_report(target: str, findings: list, config: dict) -> str:
    ai_config = config.get('ai_engine', {})
    if not ai_config.get('enabled', False):
        return None

    base_url = ai_config.get('base_url', 'http://localhost:11434/v1').rstrip('/')
    api_key = ai_config.get('api_key', 'ollama')
    model = ai_config.get('model', 'llama3')
    
    # Simplify findings to text
    findings_str = json.dumps(findings, default=str)
    
    template = ai_config.get('prompt_template', 
                           "Analyze the following OSINT data. Summarize key findings, risks, and potential connections for target: {target}.\nData: {data}")
    
    final_prompt = template.replace("{target}", target).replace("{data}", findings_str) 

    # Call API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional intelligence analyst."},
            {"role": "user", "content": final_prompt}
        ],
        "stream": False
    }

    try:
        loop = asyncio.get_event_loop()
        url = f"{base_url}/chat/completions"
        response = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=payload, timeout=60))
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"AI Error: API returned {response.status_code}"
            
    except Exception as e:
        return f"AI Connection Failed: {str(e)}"

if __name__ == "__main__":
    pass
